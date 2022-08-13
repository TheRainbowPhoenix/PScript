//
// Created by Phoebe on 14/08/2022.
//

#ifndef CMAKE_GC_H
#define CMAKE_GC_H

#define STACK_MAX 256
#define INIT_OBJ_NUM_MAX 8

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

VM* newVM(void);

void push(VM* vm, Object* value);
Object* pop(VM* vm);
void mark(Object* object);

void markAll(VM* vm);
void sweep(VM* vm);
void gc(VM* vm);
Object* newObject(VM* vm, ObjectType type);
void pushInt(VM* vm, int intValue);
Object* pushPair(VM* vm);
void objectPrint(Object* object);
void freeVM(VM *vm);

#endif //CMAKE_GC_H
