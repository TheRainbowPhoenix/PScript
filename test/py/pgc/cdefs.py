import os
import ctypes

from .consts import STACK_MAX

(OBJ_INT, OBJ_PAIR) = map(ctypes.c_uint, range(2))

ObjectType = ctypes.c_uint

class Object(ctypes.Structure):
    pass


class ObjectPair(ctypes.Structure):
    _fields_ = [
        ('head', ctypes.POINTER(Object)),
        ('tail', ctypes.POINTER(Object))
    ]


class ObjectUnion(ctypes.Union):
    _anonymous_ = [
        'pair'
    ]
    _fields_ = [
        ('value', ctypes.c_int),
        ('pair', ObjectPair)
    ]


Object._anonymous_ = [
    'types'
]

Object._fields_ = [
    ("type", ObjectType),
    ("marked", ctypes.c_char),
    ("next", ctypes.POINTER(Object)),
    ("types", ObjectUnion)
]


class VM(ctypes.Structure):
    _fields_ = [
        ("stack", ctypes.POINTER(Object) * STACK_MAX),
        ("stackSize", ctypes.c_int),
        ("firstObject", ctypes.POINTER(Object)),
        ("numObjects", ctypes.c_int),
        ("maxObjects", ctypes.c_int)
    ]