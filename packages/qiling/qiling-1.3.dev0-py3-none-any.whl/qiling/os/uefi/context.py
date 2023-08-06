from abc import ABC

from qiling.os.memory import QlMemoryHeap
from qiling.os.uefi.utils import init_struct, str_to_guid
from qiling.os.uefi.UefiSpec import EFI_CONFIGURATION_TABLE, EFI_SYSTEM_TABLE
from qiling.os.uefi.smst import EFI_SMM_SYSTEM_TABLE2

class UefiContext(ABC):
	def __init__(self, ql):
		self.ql = ql
		self.heap = None
		self.protocols = {}

		# These members must be initialized before attempting to install a configuration table.
		self.conf_table_array = []
		self.conf_table_array_ptr = 0
		self.conf_table_data_ptr = 0
		self.conf_table_data_next_ptr = 0

	def init_heap(self, base, size):
		self.heap = QlMemoryHeap(self.ql, base, base + size)

	def init_stack(self, base, size):
		self.ql.mem.map(base, size)

	def install_protocol(self, proto_desc, handle, address=None):
		guid = proto_desc['guid']

		if handle not in self.protocols:
			self.protocols[handle] = {}

		if guid in self.protocols[handle]:
			self.ql.log.warning(f'a protocol with guid {guid} is already installed')

		if address is None:
			struct_class = proto_desc['struct']
			address = self.heap.alloc(struct_class.sizeof())

		instance = init_struct(self.ql, address, proto_desc)
		instance.saveTo(self.ql, address)

		self.protocols[handle][guid] = address

	def install_configuration_table(self, guid, table):
		guid = guid.lower()
		confs = self.conf_table_array

		# find configuration table entry by guid. if found, idx would be set to the entry index
		# in the array. if not, idx would be set to one past end of array
		if guid not in confs:
			confs.append(guid)
			
		idx = confs.index(guid)
		ptr = self.conf_table_array_ptr + (idx * EFI_CONFIGURATION_TABLE.sizeof())

		instance = EFI_CONFIGURATION_TABLE()
		instance.VendorGuid = str_to_guid(guid)
		instance.VendorTable = table
		instance.saveTo(self.ql, ptr)

class DxeContext(UefiContext):
	def install_configuration_table(self, guid, table):
		super().install_configuration_table(guid, table)
		# Update number of configuration table entries in the ST.
		gST = EFI_SYSTEM_TABLE.loadFrom(self.ql, self.ql.loader.gST)
		gST.NumberOfTableEntries = len(self.conf_table_array)
		gST.saveTo(self.ql, self.ql.loader.gST)

class SmmContext(UefiContext):
	def __init__(self, ql):
		super(SmmContext, self).__init__(ql)

		# assume tseg is inaccessible to non-smm
		self.tseg_open = False

		# assume tseg is locked
		self.tseg_locked = True

		self.swsmi_handlers = []

	def install_configuration_table(self, guid, table):
		super().install_configuration_table(guid, table)
		# Update number of configuration table entries in the SMST.
		gSmst = EFI_SMM_SYSTEM_TABLE2.loadFrom(self.ql, self.ql.loader.gSmst)
		gSmst.NumberOfTableEntries = len(self.conf_table_array)
		gSmst.saveTo(self.ql, self.ql.loader.gSmst)
