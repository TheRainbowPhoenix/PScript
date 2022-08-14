import enum
import os
import sys
import ctypes

""" ==================================
>  Path config and globals
================================== """


# path = os.path.dirname(os.path.abspath(__file__))
path = "."

if not any([i.startswith("libgc") for i in os.listdir(path)]):
    raise RuntimeError("No lib found in current folder.")

STACK_MAX = 256

""" ==================================
>  CTypes definition and C structures
================================== """

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

# libgc = ctypes.cdll.LoadLibrary(f'{path}/libgc.dll')
libgc_lb = ctypes.CDLL(f'{path}/libgc')
# libgc_dll = ctypes.WinDLL(f'{path}/libgc.dll', winmode=0)

""" ==================================
>  Symbols de-mangling
================================== """

libgc_lb.newVM.argtypes = []
libgc_lb.newVM.restype = ctypes.POINTER(VM)

libgc_lb.pushInt.argtypes = [ctypes.POINTER(VM), ctypes.c_int]
libgc_lb.pushInt.restype = None

libgc_lb.pushPair.argtypes = [ctypes.POINTER(VM)]
libgc_lb.pushPair.restype = ctypes.POINTER(Object)

libgc_lb.gc.argtypes = [ctypes.POINTER(VM)]
libgc_lb.gc.restype = None

libgc_lb.freeVM.argtypes = [ctypes.POINTER(VM)]
libgc_lb.freeVM.restype = None

libgc_lb.pop.argtypes = [ctypes.POINTER(VM)]
libgc_lb.pop.restype = ctypes.POINTER(Object)

libgc_lb.objectPrint.argtypes = [ctypes.POINTER(Object)]
libgc_lb.objectPrint.restype = None


class GC_VM:
    """
    Python class wrapper around our GC Virtual Machine
    """
    def __init__(self):
        self._freed = False
        self._vm: ctypes.POINTER(VM) = libgc_lb.newVM()

    def __del__(self):
        if not self._freed:
            self.free()

    def pushInt(self, val: int):
        """
        Push a int value into the VM stack
        :param val: 32 bits signed integer
        """
        libgc_lb.pushInt(self._vm, ctypes.c_int(val))

    def pushPair(self) -> ctypes.POINTER(Object):
        """
        Push a pair into the VM from the two last integer on stack
        :return: Pointer to the pair
        """
        return libgc_lb.pushPair(self._vm)

    def pop(self) -> ctypes.POINTER(Object):
        """
        Pop last value from stack
        :return: Pointer to the object (integer, pair ...)
        """
        return libgc_lb.pop(self._vm)

    def gc(self):
        """
        Force a GC cycle on the VM
        """
        libgc_lb.gc(self._vm)

    def free(self):
        """
        Terminate the execution and clean the VM
        :raise RuntimeError when freed more than once
        """
        if not self._freed:
            libgc_lb.freeVM(self._vm)
            self._freed = True
        else:
            raise RuntimeError("Double free on VM")

    def dump_stack(self):
        print("Stack dump:\n")

        for i in range(self._vm.contents.stackSize):
            o_p: ctypes.POINTER(Object) = self._vm.contents.stack[i]

            print(f'{i:02x}'.upper(), end='  ')
            libgc_lb.objectPrint(o_p)
            print(' ')
        pass

# ======================================================================================================================
# Tests begins here
# If you use this script, remove the following lines
# ======================================================================================================================


def test1():
    print("=== Test 1: Objects on stack are preserved. ===")
    vm = GC_VM()

    vm.pushInt(1)
    vm.pushInt(2)
    vm.gc()
    assert vm._vm.contents.numObjects == 2, "[!] Should have preserved objects."
    vm.free()


def test2():
    print("=== Test 2: Unreached objects are collected. ===")
    vm = GC_VM()

    vm.pushInt(1)
    vm.pushInt(2)

    o2 = vm.pop()
    o1 = vm.pop()

    # print(o1.contents.value)
    # print(o2.contents.value)

    vm.gc()
    assert vm._vm.contents.numObjects == 0, "[!] Should have collected objects."
    vm.free()


def test3():
    print("=== Test 3: Reach nested objects. ===")
    vm = GC_VM()

    vm.pushInt(1)
    vm.pushInt(2)
    p1 = vm.pushPair()
    vm.pushInt(3)
    vm.pushInt(4)
    p2 = vm.pushPair()
    p3 = vm.pushPair()

    vm.gc()
    assert vm._vm.contents.numObjects == 7, "[!] Should have reached objects."

    # p1.contents.head.contents.value == 1
    # p1.contents.tail.contents.value == 2

    vm.free()


def test4():
    print("=== Test 4: Handle cycles. === ")
    vm = GC_VM()

    vm.pushInt(1)
    vm.pushInt(2)
    a: ctypes.POINTER(Object) = vm.pushPair()
    vm.pushInt(3)
    vm.pushInt(4)
    b: ctypes.POINTER(Object) = vm.pushPair()

    # Set up a cycle, and also make 2 and 4 unreachable and collectible
    a.contents.tail = b
    b.contents.tail = a

    vm.gc()
    assert vm._vm.contents.numObjects == 4, "[!] Should have collected objects."

    vm.free()


def test_stack():
    print("=== Test Stack ===")
    vm = GC_VM()

    for i in range(30):
        vm.pushInt(i)
        if 5 < i % 10 < 8 or (i>4 and i%3==0):
            vm.pushPair()

    vm.dump_stack()

    vm.gc()
    vm.free()


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test_stack()
