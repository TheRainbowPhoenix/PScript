import ctypes
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

try:
    from .pgc import load_lib, GC_VM, Object, OBJ_INT, OBJ_PAIR
except:
    from pgc import load_lib, GC_VM, Object, OBJ_INT, OBJ_PAIR


class PEvalSubset:
    def __init__(self):
        self.vm: GC_VM = None

    def binary_func(self, w: ctypes.POINTER(Object), v: ctypes.POINTER(Object), operator: str) -> int:
        if w.contents.type == OBJ_INT.value and v.contents.type == OBJ_INT.value:
            if operator == "-":
                return v.contents.value - w.contents.value
            elif operator == "+":
                # Add can concat strings too
                return v.contents.value + w.contents.value

        print(f"Unknown operator \"{operator}\" for types w:{w.contents.type}, v:{v.contents.type}")

    def BINARY_SUBTRACT(self):
        w: ctypes.POINTER(Object) = self.vm.pop()
        v: ctypes.POINTER(Object) = self.vm.pop()

        x = self.binary_func(w, v, "-")

        self.vm.pushInt(x)

    def BINARY_ADD(self):
        w: ctypes.POINTER(Object) = self.vm.pop()
        v: ctypes.POINTER(Object) = self.vm.pop()

        x = self.binary_func(w, v, "+")

        self.vm.pushInt(x)

    def test_op(self):
        self.vm = GC_VM("../../bin")

        # Doing simple calculations: 15-5+2
        self.vm.pushInt(15)
        self.vm.pushInt(5)

        self.BINARY_SUBTRACT()

        self.vm.pushInt(2)

        self.BINARY_ADD()

        self.vm.dump_stack()

        res = self.vm.pop().contents.value

        print(res)

        self.vm.gc()
        self.vm.free()


if __name__ == '__main__':
    pe = PEvalSubset()
    pe.test_op()
