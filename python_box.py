'''
@Project : treasure-box 
@File    : python_box.py
@Author  : luojiaaoo
@Page    : https://github.com/luojiaaoo
@Link    : https://github.com/luojiaaoo/treasure-box
'''
####################################################
ANNOTATION = """类的懒加载"""
####################################################
from importlib import import_module

class LazyImport:
    def __init__(self, module_name):
        self._module_name = module_name
        self._module = None

    def __getattr__(self, attr):
        if self._module is None:
            self._module = import_module(self._module_name)
        return getattr(self._module, attr)

####################################################
ANNOTATION = """用于在Python里进行C的移位/与/或/非操作"""
####################################################
from ctypes import c_uint8, c_uint16, c_uint32, _SimpleCData
from typing import Generic, TypeVar, Type

T = TypeVar("T", bound=_SimpleCData)


class CUInt(Generic[T]):
    def __init__(self, value, type_c_uint: Type[T]):
        self.type_c_uint = type_c_uint
        self.data = self.type_c_uint(value)

    def type_to(self, type_c_uint: Type[T]):
        return CUInt(self.value, type_c_uint)

    @property
    def value(self):
        return self.data.value

    def __int__(self):
        return self.value

    def __rshift__(self, bit_count: int):
        return CUInt(self.value >> bit_count, self.type_c_uint)

    def __lshift__(self, bit_count: int):
        return CUInt(self.value << bit_count, self.type_c_uint)
    
    def __add__(self, cuint: "CUInt[T]"):
        if cuint.type_c_uint != self.type_c_uint:
            raise ValueError(
                f"Error: type_c_uint is not equal, type_c_uint={self.type_c_uint}, cuint.type_c_uint={cuint.type_c_uint}"
            )
        return CUInt(self.value + cuint.value, self.type_c_uint)
    
    def __sub__(self, cuint: "CUInt[T]"):
        if cuint.type_c_uint != self.type_c_uint:
            raise ValueError(
                f"Error: type_c_uint is not equal, type_c_uint={self.type_c_uint}, cuint.type_c_uint={cuint.type_c_uint}"
            )
        return CUInt(self.value - cuint.value, self.type_c_uint)

    def __and__(self, cuint: "CUInt[T]"):
        if cuint.type_c_uint != self.type_c_uint:
            raise ValueError(
                f"Error: type_c_uint is not equal, type_c_uint={self.type_c_uint}, cuint.type_c_uint={cuint.type_c_uint}"
            )
        return CUInt(self.value & cuint.value, self.type_c_uint)

    def __or__(self, cuint: "CUInt[T]"):
        if cuint.type_c_uint != self.type_c_uint:
            raise ValueError(
                f"Error: type_c_uint is not equal, type_c_uint={self.type_c_uint}, cuint.type_c_uint={cuint.type_c_uint}"
            )
        return CUInt(self.value | cuint.value, self.type_c_uint)

    def __xor__(self, cuint: "CUInt[T]"):
        if cuint.type_c_uint != self.type_c_uint:
            raise ValueError(
                f"Error: type_c_uint is not equal, type_c_uint={self.type_c_uint}, cuint.type_c_uint={cuint.type_c_uint}"
            )
        return CUInt(self.value ^ cuint.value, self.type_c_uint)

    def __invert__(self):
        return CUInt(~self.value, self.type_c_uint)


import numpy as np

for _ in range(1000):
    from random import randint

    list_uint8 = [randint(0, 255) for _ in range(4)]
    a = (
        np.uint32(list_uint8[0]) << np.uint32(24)
        | ~np.uint32(list_uint8[1]) << np.uint32(16)
        | np.uint32(list_uint8[2]) >> np.uint32(8) & np.uint32(list_uint8[3])
    )
    b = (
        CUInt(list_uint8[0], c_uint32) << 24
        | ~CUInt(list_uint8[1], c_uint32) << 16
        | CUInt(list_uint8[2], c_uint32) >> 8 & CUInt(list_uint8[3], c_uint32)
    ).value()
    if a != b:
        raise ValueError(f"Error: {a} != {b}, list_uint8={list_uint8}")
    else:
        print(f"Success: {a} == {b}, list_uint8={list_uint8}")

#############################
ANNOTATION = """异常重试装饰器"""
#############################

from functools import wraps
from time import sleep
from typing import Tuple


def retry(exceptions: Tuple[Exception], retries: int = 3, delay: float = 1):
    """
    函数执行失败时，重试

    :param retries: 最大重试的次数
    :param delay: 每次重试的间隔时间，单位 秒
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 第一次正常执行不算重试次数，所以retries+1
            for i in range(retries + 1):
                if i == retries:
                    return func(*args, **kwargs)
                else:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        sleep(delay)

        return wrapper

    return decorator


####################################################
ANNOTATION = """每60秒瞬间切换大小写，保证电脑不休眠线程"""
####################################################

import os
import threading
import time
import win32api
import win32con

def start_thread_to_avoid_sleep_windows():
    th = threading.Thread(target=mouse_move)
    th.setDaemon(True)
    th.start()

def mouse_move():
    while True:
        win32api.keybd_event(0x14, 0, 0, 0)
        win32api.keybd_event(0x14, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x14, 0, 0, 0)
        win32api.keybd_event(0x14, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(60)
