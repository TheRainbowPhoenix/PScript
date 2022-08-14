//
// Created by Phoebe on 14/08/2022.
//

#ifndef CMAKE_GC_H
#define CMAKE_GC_H

#define STACK_MAX 256
#define INIT_OBJ_NUM_MAX 8

#define EXPORTED __declspec(dllexport)

typedef enum {
    OBJ_INT,
    OBJ_PAIR
} ObjectType;

typedef struct sObject {
    ObjectType type;
    unsigned char marked;

    /* The next object in the linked list of heap allocated objects. */
    struct sObject* next;

    union {
        /* OBJ_INT */
        int value;

        /* OBJ_PAIR */
        struct {
            struct sObject* head;
            struct sObject* tail;
        };
    };
} Object;

typedef struct {
    Object* stack[STACK_MAX];
    int stackSize;

    /* The first object in the linked list of all objects on the heap. */
    Object* firstObject;

    /* The total number of currently allocated objects. */
    int numObjects;

    /* The number of objects required to trigger a GC. */
    int maxObjects;
} VM;

// TODO: move me ?
void assert(int condition, const char* message);

// Functions headers

EXPORTED VM* newVM(void);

EXPORTED void push(VM* vm, Object* value);
EXPORTED Object* pop(VM* vm);
EXPORTED void mark(Object* object);

EXPORTED void markAll(VM* vm);
EXPORTED void sweep(VM* vm);
EXPORTED void gc(VM* vm);
EXPORTED Object* newObject(VM* vm, ObjectType type);
EXPORTED void pushInt(VM* vm, int intValue);
EXPORTED Object* pushPair(VM* vm);
EXPORTED void objectPrint(Object* object);
EXPORTED void freeVM(VM *vm);

#endif //CMAKE_GC_H
