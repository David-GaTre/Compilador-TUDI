from memory import GLOBAL_START, LOCAL_START, TEMP_START, CONST_START, CONST_LIMIT, Memory, FunctionMemory
from collections import deque

class VirtualMachine():
    def __init__(self, func_dir, quadruples, v_mem) -> None:
        self.virtual_memory = v_mem
        self.virtual_memory.start_memory(func_dir)
        self.quadruples = quadruples
        self.counter = 0
        self.curr_func = FunctionMemory()
        self.programFuncs = deque()

    def start_machine(self):
        while self.counter < len(self.quadruples):
            print(self.counter + 1)
            self.do_action(self.quadruples[self.counter])
            self.counter += 1 # Going to next quadruple
    
    def do_action(self, quadruple):
        if quadruple.operator == '+':
            temp_val = self.get_address_value(quadruple.left_operand).value + self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '-':
            temp_val = self.get_address_value(quadruple.left_operand).value - self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '*':
            temp_val = self.get_address_value(quadruple.left_operand).value * self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '/':
            temp_val = self.get_address_value(quadruple.left_operand).value / self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == 'y':
            temp_val = self.get_address_value(quadruple.left_operand).value and self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == 'o':
            temp_val = self.get_address_value(quadruple.left_operand).value or self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '>=':
            temp_val = self.get_address_value(quadruple.left_operand).value >= self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '<=':
            temp_val = self.get_address_value(quadruple.left_operand).value <= self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '>':
            temp_val = self.get_address_value(quadruple.left_operand).value > self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '<':
            temp_val = self.get_address_value(quadruple.left_operand).value < self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '!=':
            temp_val = self.get_address_value(quadruple.left_operand).value != self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '==':
            temp_val = self.get_address_value(quadruple.left_operand).value == self.get_address_value(quadruple.right_operand).value
            self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
        elif quadruple.operator == '=':
            if quadruple.temp >= GLOBAL_START and quadruple.temp < LOCAL_START:
                self.set_global_var(quadruple.temp, self.get_address_value(quadruple.left_operand).value)
            else:
                temp_val = self.get_address_value(quadruple.left_operand).value
                if quadruple.temp not in self.programFuncs[-1].temp_memory:
                    self.programFuncs[-1].temp_memory[quadruple.temp] = Memory(quadruple.temp, temp_val)
                else:
                    self.programFuncs[-1].temp_memory[quadruple.temp].value = temp_val
        #elif quadruple.operator == 'Read':
        #    pass
        elif quadruple.operator == 'Print':
            print(self.get_address_value(quadruple.temp).value)
        elif quadruple.operator == 'GOTO':
            self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOTO_F':
            if not self.get_address_value(quadruple.left_operand).value:
                self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOTO_V':
            if self.get_address_value(quadruple.left_operand).value:
                self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOSUB':
            self.programFuncs.append(self.virtual_memory.func_call_stack[-1])
            self.curr_func = self.virtual_memory.func_call_stack[-1]
            self.curr_func.prev_func = self.counter
            self.counter = self.curr_func.start-2
        elif quadruple.operator == 'ENDFUNC':
            if self.programFuncs:
                self.programFuncs.pop()
            self.curr_func = self.virtual_memory.func_call_stack[-1]
            self.counter = self.curr_func.prev_func
            self.virtual_memory.func_call_stack.pop()
        elif quadruple.operator == 'ERA':
            new_func = self.virtual_memory.new_function_memory(quadruple.temp)
            self.virtual_memory.func_call_stack.append(new_func)          
        else:
            print("Not yet handled")

    def get_address_value(self, address):
        if address >= CONST_START:
            return self.virtual_memory.constant_table[address]
        # Locals and temps
        elif address >= LOCAL_START and address < CONST_START:
            temp_memory = self.programFuncs[-1].temp_memory
            return temp_memory[address]
        elif address >= GLOBAL_START and address < LOCAL_START:
            value = None
            for p in self.virtual_memory.func_call_stack:
                if p.func_name == "0":
                    return p.temp_memory[address]
            return value
        
    def set_global_var(self, address,value):
        for p in self.virtual_memory.func_call_stack:
            if p.func_name == "0":
                p.temp_memory[address] = Memory(address, value)

    def get_global_var(self, address):
        for p in self.virtual_memory.func_call_stack:
            if p.func_name == "0":
                return p.temp_memory[address]
    

