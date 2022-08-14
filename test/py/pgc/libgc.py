import ctypes

from .cdefs import VM, Object


def load_lib(path: str, name: str = "libgc"):
    """
    Load libgc and demangle it
    :param path: path where the libgc is located
    :param name: name of the libgc dll
    """
    libgc_lb = ctypes.CDLL(f'{path}/{name}')

    return _demangle_lib(libgc_lb)


def _demangle_lib(libgc_lb):
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

    return libgc_lb
