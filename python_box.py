"""
用于在Python里进行C的移位/与/或/非操作
"""
import ctypes
from typing import Generic, TypeVar, Type

T = TypeVar("T", bound=ctypes._SimpleCData)


class CUInt(Generic[T]):
    def __init__(self, value, type_c_uint: Type[T]):
        self.type_c_uint = type_c_uint
        self.data = self.type_c_uint(value)

    def type_to(self, type_c_uint: Type[T]):
        return CUInt(self.value(), type_c_uint)

    def value(self):
        return self.data.value

    def __rshift__(self, bit_count: int):
        return CUInt(self.value() >> bit_count, self.type_c_uint)

    def __lshift__(self, bit_count: int):
        return CUInt(self.value() << bit_count, self.type_c_uint)

    def __and__(self, cuint: "CUInt[T]"):
        return CUInt(self.value() & cuint.value(), self.type_c_uint)

    def __or__(self, cuint: "CUInt[T]"):
        return CUInt(self.value() | cuint.value(), self.type_c_uint)
    
    def __invert__(self):
        return CUInt(~self.value(), self.type_c_uint)


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
        CUInt(list_uint8[0], ctypes.c_uint32) << 24
        | ~CUInt(list_uint8[1], ctypes.c_uint32) << 16
        | CUInt(list_uint8[2], ctypes.c_uint32) >> 8 & CUInt(list_uint8[3], ctypes.c_uint32)
    ).value()
    if a != b:
        raise ValueError(f"Error: {a} != {b}, list_uint8={list_uint8}")
    else:
        print(f"Success: {a} == {b}, list_uint8={list_uint8}")
