import dis
import gc

def cond():
    x = 3
    if x < 5:
        return 'yes'
    else:
        return 'no'

what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),  # the first number
                     ("LOAD_VALUE", 1),  # the second number
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5]
}


bytc = cond.__code__.co_code
print(bytc)
list(bytc)
print(list(bytc))

dis.dis(cond)

for i in range(0, len(bytc), 2):
    line = ' '
    op_name = dis.opname[bytc[i]]
    var = bytc[i+1]

    var_disp = ''

    if "LOAD_" in op_name:
        var_disp = f'{var:>4} (0)'
    if "STORE_" in op_name:
        var_disp = f'{var:>4} (x)'

    print(f'{line:>3}  {i:>10} {op_name:<22}{var_disp}')

class Interpreter:
    def __init__(self):
        self.stack = []

    def LOAD_VALUE(self, number):
        self.stack.append(number)
        self.environment = {}

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.environment[name] = val

    def LOAD_NAME(self, name):
        val = self.environment[name]
        self.stack.append(val)

    def parse_argument(self, instruction, argument, what_to_execute):
        """ Understand what the argument to each instruction means."""
        numbers = ["LOAD_VALUE"]
        names = ["LOAD_NAME", "STORE_NAME"]

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)

            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argument)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == "STORE_NAME":
                self.STORE_NAME(argument)
            elif instruction == "LOAD_NAME":
                self.LOAD_NAME(argument)

    def execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)

if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
