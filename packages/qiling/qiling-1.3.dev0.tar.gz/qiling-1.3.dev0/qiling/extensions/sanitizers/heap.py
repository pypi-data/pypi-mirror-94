#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import random
from enum import Enum

class CaneryType(Enum):
        underflow = 0
        overflow = 1
        uaf = 2

class QlSanitizedMemoryHeap():
    """
    Clients can enable the santized heap using the following snippet:

    ql.os.heap = qiling.os.memory.QlSanitizedMemoryHeap(ql, ql.os.heap)
    ql.os.heap.oob_handler = my_oob_handler
    ql.os.heap.bo_handler = my_bo_handler
    ql.os.heap.bad_free_handler = my_bad_free_handler
    ql.os.heap.uaf_handler = my_uaf_handler
    """

    def __init__(self, ql, heap, fault_rate=0, canary_byte=b'\xCD'):
        self.ql = ql
        self.heap = heap
        self.fault_rate = fault_rate
        self.canary_byte = canary_byte
        self.canaries = []

    def save(self):
        saved_state = {}
        saved_state['heap'] = self.heap.save()
        saved_state['fault_rate'] = self.fault_rate
        saved_state['canary_byte'] = self.canary_byte
        saved_state['canaries'] = self.canaries
        return saved_state

    def restore(self, saved_state):
        self.heap.restore(saved_state['heap'])
        self.fault_rate = saved_state['fault_rate']
        self.canary_byte = saved_state['canary_byte']
        self.canaries = saved_state['canaries']
        for (canary_begin, canary_end, canery_type) in self.canaries:
            if canery_type == CaneryType.underflow or canery_type == CaneryType.overflow:
                self.ql.hook_mem_write(self.bo_handler, begin=canary_begin, end=canary_end)
                self.ql.hook_mem_read(self.oob_handler, begin=canary_begin, end=canary_end)
            else:
                self.ql.hook_mem_valid(self.uaf_handler, begin=canary_begin, end=canary_end)

    @staticmethod
    def bo_handler(ql, access, addr, size, value):
        """
        Called when a buffer overflow/underflow is detected.
        """
        pass

    @staticmethod
    def oob_handler(ql, access, addr, size, value):
        """
        Called when an out-of-bounds element is accessed.
        """
        pass

    @staticmethod
    def uaf_handler(ql, access, addr, size, value):
        """
        Called when a use-after-free is detected.
        """
        pass

    @staticmethod
    def bad_free_handler(ql, addr):
        """
        Called when a bad/double free is detected.
        """
        pass

    def alloc(self, size):
        chance = random.randint(1, 100)
        if chance <= self.fault_rate:
            # Fail the allocation.
            return 0

        # Add 8 bytes to the requested size so as to accomodate the canaries.
        addr = self.heap.alloc(size + 8)
        self.ql.mem.write(addr, self.canary_byte * (size + 8))

        # Install canary hooks for overflow/underflow detection.
        underflow_canary = (addr, addr + 3, CaneryType.underflow)
        self.ql.hook_mem_write(self.bo_handler, begin=underflow_canary[0], end=underflow_canary[1])
        self.ql.hook_mem_read(self.oob_handler, begin=underflow_canary[0], end=underflow_canary[1])
        self.canaries.append(underflow_canary)

        overflow_canary = (addr + 4 + size, addr + 4 + size + 3, CaneryType.overflow)
        self.ql.hook_mem_write(self.bo_handler, begin=overflow_canary[0], end=overflow_canary[1])
        self.ql.hook_mem_read(self.oob_handler, begin=overflow_canary[0], end=overflow_canary[1])
        self.canaries.append(overflow_canary)

        return (addr + 4)

    def size(self, addr):
        return self.heap.size(addr - 4)

    def free(self, addr):
        chunk = self.heap._find(addr - 4)

        if not chunk:
            self.bad_free_handler(self.ql, addr)
            return False

        # Install the UAF canary hook.
        self.ql.mem.write(addr, self.canary_byte * (chunk.size - 8))
        uaf_canary = (addr, addr + chunk.size - 8 - 1, CaneryType.uaf)
        self.ql.hook_mem_valid(self.uaf_handler, begin=uaf_canary[0], end=uaf_canary[1])
        self.canaries.append(uaf_canary)

        # Make sure the chunk won't be re-used by the underlying heap.
        self.heap.chunks.remove(chunk)
        return True

    def validate(self):
        for (canary_begin, canary_end, canery_type) in self.canaries:
            size = canary_end - canary_begin + 1
            canary = self.ql.mem.read(canary_begin, size)
            if canary.count(self.canary_byte) != len(canary):
                return False
        return True
        