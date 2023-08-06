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

@winsdkapi(cc=STDCALL)
def hook_WudfIsUserDebuggerPresent(ql, address, params):
    return 0


@winsdkapi(cc=STDCALL)
def hook_WudfIsAnyDebuggerPresent(ql, address, params):
    return 0


@winsdkapi(cc=STDCALL)
def hook_WudfIsKernelDebuggerPresent(ql, address, params):
    return 0
