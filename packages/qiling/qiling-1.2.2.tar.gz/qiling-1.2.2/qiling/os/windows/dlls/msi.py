#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import struct
from qiling.os.windows.const import *
from qiling.os.windows.fncc import *
from qiling.os.const import *
from qiling.os.windows.utils import *
from qiling.os.windows.thread import *
from qiling.os.windows.handle import *
from qiling.exception import *

dllname = 'msi_dll'

# UINT MsiGetComponentStateA(
#   MSIHANDLE    hInstall,
#   LPCSTR       szComponent,
#   INSTALLSTATE *piInstalled,
#   INSTALLSTATE *piAction
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_MsiGetComponentStateA(ql, address, params):
    return 6  # INVALID_HANDLE
