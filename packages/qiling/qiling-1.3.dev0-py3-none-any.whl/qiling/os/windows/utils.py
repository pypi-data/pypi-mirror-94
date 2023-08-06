#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import ntpath, os, uuid

from sys import getsizeof

from qiling.const import *

from qiling.os.const import *
from .registry import RegistryManager
from .clipboard import Clipboard
from .fiber import FiberManager
from .handle import HandleManager, Handle
from .thread import QlWindowsThreadManagement, QlWindowsThread
from .structs import UNICODE_STRING32, UNICODE_STRING64


def ql_x86_windows_hook_mem_error(ql, access, addr, size, value):
    ql.log.debug("ERROR: unmapped memory access at 0x%x" % addr)
    return False


def string_unpack(string):
    return string.decode().split("\x00")[0]


def read_guid(ql, address):
    result = ""
    raw_guid = ql.mem.read(address, 16)
    return uuid.UUID(bytes_le=bytes(raw_guid))


def env_dict_to_array(env_dict):
    env_list = []
    for item in env_dict:
        env_list.append(item + "=" + env_dict[item])
    return env_list


def debug_print_stack(ql, num, message=None):
    if message:
        ql.log.debug("========== %s ==========" % message)
        sp = ql.reg.arch_sp
        ql.log.debug(hex(sp + ql.pointersize * num) + ": " + hex(ql.stack_read(num * ql.pointersize)))


def is_file_library(string):
    string = string.lower()
    extension = string[-4:]
    return extension in (".dll", ".exe", ".sys", ".drv")


def string_to_hex(string):
    return ":".join("{:02x}".format(ord(c)) for c in string)


def string_appearance(ql, string):
    strings = string.split(" ")
    for string in strings:
        val = ql.os.appeared_strings.get(string, set())
        val.add(ql.os.syscalls_counter)
        ql.os.appeared_strings[string] = val


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def find_size_function(ql, func_addr):
    # We have to retrieve the return address position
    code = ql.mem.read(func_addr, 0x100)
    return_procedures = [b"\xc3", b"\xc2", b"\xcb", b"\xca"]
    min_index = min([code.index(return_value) for return_value in return_procedures if return_value in code])
    return min_index
