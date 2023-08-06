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
from qiling.os.windows.structs import *
from qiling.const import *


dllname = 'kernel32_dll'

# void Sleep(
#  DWORD dwMilliseconds
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_Sleep(ql, address, params):
    # time.sleep(params["dwMilliseconds"] * 10**(-3))
    pass


# void EnterCriticalSection(
#  LPCRITICAL_SECTION lpCriticalSection
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_EnterCriticalSection(ql, address, params):
    return 0


# void LeaveCriticalSection(
#  LPCRITICAL_SECTION lpCriticalSection
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_LeaveCriticalSection(ql, address, params):
    return 0


# void DeleteCriticalSection(
#   LPCRITICAL_SECTION lpCriticalSection
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_DeleteCriticalSection(ql, address, params):
    return 0


# void InitializeCriticalSection(
#   LPCRITICAL_SECTION lpCriticalSection
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_InitializeCriticalSection(ql, address, params):
    return 1


# BOOL InitializeCriticalSectionEx(
#   LPCRITICAL_SECTION lpCriticalSection,
#   DWORD              dwSpinCount,
#   DWORD              Flags
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_InitializeCriticalSectionEx(ql, address, params):
    return 1


# BOOL InitializeCriticalSectionAndSpinCount(
#  LPCRITICAL_SECTION lpCriticalSection,
#  DWORD              dwSpinCount
# );
@winsdkapi(cc=STDCALL, dllname=dllname, replace_params_type={'DWORD': 'UINT'})
def hook_InitializeCriticalSectionAndSpinCount(ql, address, params):
    return 1


# DWORD WaitForSingleObject(
#   HANDLE hHandle,
#   DWORD  dwMilliseconds
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_WaitForSingleObject(ql, address, params):
    ret = 0
    hHandle = params["hHandle"]
    dwMilliseconds = params["dwMilliseconds"]

    handle = ql.os.handle_manager.get(hHandle)
    if handle:
        target_thread = handle.obj
        ql.os.thread_manager.cur_thread.waitfor(target_thread)

    return ret


# DWORD WaitForSingleObjectEx(
#   HANDLE hHandle,
#   DWORD  dwMilliseconds
#   BOOL   bAlertable
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_WaitForSingleObjectEx(ql, address, params):
    ret = 0
    hHandle = params["hHandle"]
    dwMilliseconds = params["dwMilliseconds"]
    alertable = params["bAlertable"]

    target_thread = ql.os.handle_manager.get(hHandle).obj
    ql.os.thread_manager.cur_thread.waitfor(target_thread)

    return ret


# DWORD WaitForMultipleObjects(
#   DWORD        nCount,
#   const HANDLE *lpHandles,
#   BOOL         bWaitAll,
#   DWORD        dwMilliseconds
# );
@winsdkapi(cc=STDCALL, dllname=dllname, replace_params_type={'HANDLE': 'POINTER'})
def hook_WaitForMultipleObjects(ql, address, params):
    ret = 0
    nCount = params["nCount"]
    lpHandles = params["lpHandles"]
    bWaitAll = params["bWaitAll"]
    dwMilliseconds = params["dwMilliseconds"]

    for i in range(nCount):
        handle_value = ql.unpack(ql.mem.read(lpHandles + i * ql.pointersize, ql.pointersize))
        if handle_value != 0:
            thread = ql.os.handle_manager.get(handle_value).obj
            ql.os.thread_manager.cur_thread.waitfor(thread)

    return ret


# HANDLE OpenMutexW(
#   DWORD   dwDesiredAccess,
#   BOOL    bInheritHandle,
#   LPCWSTR lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_OpenMutexW(ql, address, params):
    # The name can have a "Global" or "Local" prefix to explicitly open an object in the global or session namespace.
    # It can also have no prefix
    try:
        _type, name = params["lpName"].split("\\")
    except ValueError:
        name = params["lpName"]
        _type = ""

    handle = ql.os.handle_manager.search(name)
    if _type == "Global":
        # if is global is a Windows lock. We always return a valid handle because we have no way to emulate them
        # example sample: Gandcrab e42431d37561cc695de03b85e8e99c9e31321742
        if handle is None:
            return 0xD10C
        else:
            mutex = handle.obj
            if mutex.isFree():
                mutex.lock()
            else:
                raise QlErrorNotImplemented("API not implemented")
    else:
        if handle is None:
            # If a named mutex does not exist, the function fails and GetLastError returns ERROR_FILE_NOT_FOUND.
            ql.os.last_error = ERROR_FILE_NOT_FOUND
            return 0
        else:
            raise QlErrorNotImplemented("API not implemented")


# HANDLE OpenMutexA(
#   DWORD   dwDesiredAccess,
#   BOOL    bInheritHandle,
#   LPCSTR lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_OpenMutexA(ql, address, params):
    return hook_OpenMutexW.__wrapped__(ql, address, params)


# HANDLE CreateMutexW(
#   LPSECURITY_ATTRIBUTES lpMutexAttributes,
#   BOOL                  bInitialOwner,
#   LPCWSTR               lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_CreateMutexW(ql, address, params):
    try:
        _type, name = params["lpName"].split("\\")
    except ValueError:
        name = params["lpName"]
        _type = ""

    owning = params["bInitialOwner"]
    handle = ql.os.handle_manager.search(name)
    if handle is not None:
        # ql.os.last_error = ERROR_ALREADY_EXISTS
        return 0
    else:
        mutex = Mutex(name, _type)
        if owning:
            mutex.lock()
        handle = Handle(obj=mutex, name=name)
        ql.os.handle_manager.append(handle)

    return handle.id


# HANDLE CreateMutexA(
#   LPSECURITY_ATTRIBUTES lpMutexAttributes,
#   BOOL                  bInitialOwner,
#   LPCSTR               lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_CreateMutexA(ql, address, params):
    return hook_CreateMutexW.__wrapped__(ql, address, params)

# BOOL ReleaseMutex(
#   HANDLE hMutex
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_ReleaseMutex(ql, address, params):
    hMutex = params["hMutex"]
    handle = ql.os.handle_manager.get(hMutex)
    if not handle:
        ql.os.last_error = ERROR_INVALID_HANDLE
        return 0

    mutex = handle.obj

    if not mutex or not isinstance(mutex, Mutex):
        return 0

    if mutex.isFree():
        ql.os.last_error = ERROR_NOT_OWNER
        return 0

    # FIXME: Only the owner is allowed to do this!
    mutex.unlock()
    return 1

# HANDLE CreateEventA(
#  LPSECURITY_ATTRIBUTES lpEventAttributes,
#  BOOL                  bManualReset,
#  BOOL                  bInitialState,
#  LPCSTR                lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_CreateEventA(ql, address, params):
    """
    Implementation seems similar enough to Mutex to just use it
    """
    try:
        namespace, name = params["lpName"].split("\\")
    except ValueError:
        name = params["lpName"]
        namespace = ""
    handle = ql.os.handle_manager.search(name)
    if handle is not None:
        ql.os.last_error = ERROR_ALREADY_EXISTS
    else:
        mutex = Mutex(name, namespace)
        if params['bInitialState']:
            mutex.lock()
        handle = Handle(obj=mutex, name=name)
        ql.os.handle_manager.append(handle)
    return handle.ID


# HANDLE CreateEventW(
#  LPSECURITY_ATTRIBUTES lpEventAttributes,
#  BOOL                  bManualReset,
#  BOOL                  bInitialState,
#  LPCWSTR               lpName
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_CreateEventW(ql, address, params):
    return hook_CreateEventA.__wrapped__(ql, address, params)


# void InitializeSRWLock(
#  PSRWLOCK SRWLock
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_InitializeSRWLock(ql, address, params):
    return


# void AcquireSRWLockExclusive(
#   PSRWLOCK SRWLock
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_AcquireSRWLockExclusive(ql, address, params):
    return


# void AcquireSRWLockShared(
#   PSRWLOCK SRWLock
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_AcquireSRWLockShared(ql, address, params):
    return


# void ReleaseSRWLockExclusive(
#   PSRWLOCK SRWLock
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_ReleaseSRWLockExclusive(ql, address, params):
    return


# void ReleaseSRWLockShared(
#   PSRWLOCK SRWLock
# );
@winsdkapi(cc=STDCALL, dllname=dllname)
def hook_ReleaseSRWLockShared(ql, address, params):
    return
