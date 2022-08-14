#include <stdio.h>
#include <stdlib.h>
#include <gc.h>

int main(int argc, const char * argv[]) {
    printf("TODO: Read and interpret bytecode into VM\n");
    VM* vm = newVM();

    // TODO: interpret bytecode and push values here

    pushInt(vm, 1);
    pushInt(vm, 2);

    // TODO: sometimes GC when needed

    gc(vm);
    assert(vm->numObjects == 2, "Should have preserved objects.");

    // TODO: Don't forget to free at exit
    freeVM(vm);

  return 0;
}