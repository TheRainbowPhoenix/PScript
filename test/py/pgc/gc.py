import ctypes

from .cdefs import VM, Object
from .libgc import load_lib


class GC_VM:
    """
    Python class wrapper around our GC Virtual Machine
    """
    def __init__(self, libgc_path='.'):
        self._l = load_lib(libgc_path)
        self._freed = False
        self._vm: ctypes.POINTER(VM) = self._l.newVM()

    def __del__(self):
        if not self._freed:
            self.free()

    def pushInt(self, val: int):
        """
        Push a int value into the VM stack
        :param val: 32 bits signed integer
        """
        self._l.pushInt(self._vm, ctypes.c_int(val))

    def pushPair(self) -> ctypes.POINTER(Object):
        """
        Push a pair into the VM from the two last integer on stack
        :return: Pointer to the pair
        """
        return self._l.pushPair(self._vm)

    def pop(self) -> ctypes.POINTER(Object):
        """
        Pop last value from stack
        :return: Pointer to the object (integer, pair ...)
        """
        return self._l.pop(self._vm)

    def gc(self):
        """
        Force a GC cycle on the VM
        """
        self._l.gc(self._vm)

    def free(self):
        """
        Terminate the execution and clean the VM
        :raise RuntimeError when freed more than once
        """
        if not self._freed:
            self._l.freeVM(self._vm)
            self._freed = True
        else:
            raise RuntimeError("Double free on VM")

    def dump_stack(self):
        print("Stack dump:\n")

        for i in range(self._vm.contents.stackSize):
            o_p: ctypes.POINTER(Object) = self._vm.contents.stack[i]

            print(f'{i:02x}'.upper(), end='  ')
            self._l.objectPrint(o_p)
            print(' ')
