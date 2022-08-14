# PScript
GC attempt + fun (learning python internals and VM)

Made after reading from [journal.stuffwithstuff.com/babys-first-garbage-collector/](https://journal.stuffwithstuff.com/2013/12/08/babys-first-garbage-collector/)

Also I haven't made "serious" C/C++ for 4 years, so trying to get back to it ... 

## Installing

### With CLion

Open the cloned repo in CLion and import the CMake project.
Do `Build --> Build Project`, then 
`Build --> Install`

If python is setup, you can run `bin/testgc.py`

### Manually
First build all
`cmake --build path/to/cmake-build-debug --target all`

Then install
`cmake --build path/to/cmake-build-debug --target install`

That should place the binaries and dll into the "bin" folder

## Testing
You can run the simple `bin/pscript` client to run the latest version of the VM.
There's also the `bin/pscript_tests` binary to run extended tests.
A python script is also available.

## Working with GC
There's both a python version that uses the shared DLL version and a C version that uses the static lib with its headers.

You can take a look at `test/py/testgc.py` on how to use the lib from your python script.

### Python interface
There's a first scratch into the "testgc.py" file. You can reuse it by removing the test methods at the end and setting up your path to the libgc.

You can use it the following way :
````python
vm = GC_VM()

vm.pushInt(1)
vm.pushInt(2)

two = vm.pop()
print(f'Last stack value: {two.contents.value}')
print(f'VM Objects count: {vm._vm.contents.numObjects}')

vm.gc()
vm.free()
````

### C/C++ interface
If you want complete examples, take a look at "test/src/pscript_tests.c"

You can use it the following way :
````c++
#include <gc.h>

VM* vm = newVM();
pushInt(vm, 1);
pushInt(vm, 2);

Object* two = pop(vm);
printf("Last stack value: %d\n", two->value);
printf("VM Objects count: %d\n", vm->numObjects);

gc(vm);
freeVM(vm);
````