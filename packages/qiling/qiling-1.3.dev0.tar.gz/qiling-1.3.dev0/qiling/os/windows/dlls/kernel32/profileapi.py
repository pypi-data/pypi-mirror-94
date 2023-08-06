#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import struct
import time
from qiling.os.windows.const import *
from qiling.os.const import *
from qiling.os.windows.fncc import *
from qiling.os.windows.utils import *
from qiling.os.windows.thread import *
from qiling.os.windows.handle import *
from qiling.exception import *


dllname = 'kernel32_dll'

# BOOL QueryPerformanceCounter(
#   LARGE_INTEGER *lpPerformanceCount
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_QueryPerformanceCounter(ql, address, params):
    ret = 0
    return ret


# BOOL QueryPerformanceFrequency(
#  LARGE_INTEGER *lpFrequency
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_QueryPerformanceFrequency(ql, address, params):
    ql.mem.write(params['lpFrequency'], (10000000).to_bytes(length=8, byteorder='little'))
    return 1
