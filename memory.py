from collections import deque 
from quadruples import type_to_char, char_to_type


# NUMERIC CONSTANTS FOR MEMORY ADDRESSING
GLOBAL_INT, GLOBAL_INT_LIMIT= 0,0
GLOBAL_FLOAT, GLOBAL_FLOAT_LIMIT = 4000, 4000
GLOBAL_BOOL, GLOBAL_BOOL_LIMIT = 8000, 8000
GLOBAL_CHAR, GLOBAL_CHAR_LIMIT = 12000, 12000

LOCAL_INT, LOCAL_INT_LIMIT = 20000, 20000
LOCAL_FLOAT, LOCAL_FLOAT_LIMIT = 24000, 24000
LOCAL_BOOL, LOCAL_BOOL_LIMIT = 28000, 28000
LOCAL_CHAR, LOCAL_CHAR_LIMIT  = 32000, 32000

TEMP_INT, TEMP_INT_LIMIT = 40000, 40000
TEMP_FLOAT, TEMP_FLOAT_LIMIT = 44000, 44000
TEMP_BOOL, TEMP_BOOL_LIMIT = 48000, 48000
TEMP_CHAR, TEMP_CHAR_LIMIT = 52000, 52000
TEMP_POINTER, TEMP_POINTER_LIMIT = 56000, 56000

CONST_INT, CONST_INT_LIMIT = 60000, 60000
CONST_FLOAT, CONST_FLOAT_LIMIT = 64000, 64000
CONST_BOOL, CONST_BOOL_LIMIT = 68000, 68000
CONST_CHAR, CONST_CHAR_LIMIT  = 72000, 72000

GLOBAL_START = 0
LOCAL_START = 20000
TEMP_START = 40000
CONST_START = 60000
CONST_LIMIT = 80000 # end of memory

class Memory():
    def __init__(self, address, value):
        self.address = address
        self.value= value

    def __str__(self):
        return f'Address: {self.address}, Value: {self.value}\n'

    def __repr__(self):
        return f'Address: {self.address}, Value: {self.value}\n'

class FunctionMemory():
    def __init__(self, func_name='0', temp_memory={}, params={}, start=-1):
        self.func_name = func_name
        self.prev_func = 0
        self.temp_memory = temp_memory.copy() # Due to mutable nature
        self.params = params.copy() # Due to mutable nature
        self.start = start
    def __str__(self):
        return f'Func Name: {self.func_name}, Memory: {self.temp_memory}, Params: {self.params}\n'
    def __repr__(self):
        return f'Func Name: {self.func_name}, Memory: {self.temp_memory}, Params: {self.params}\n'

class VirtualMemory():
    def __init__(self):
        # Globales
        self.global_int_count = GLOBAL_INT
        self.global_float_count = GLOBAL_FLOAT
        self.global_bool_count = GLOBAL_BOOL
        self.global_char_count = GLOBAL_CHAR
        # Locales
        self.local_int_count = LOCAL_INT
        self.local_float_count = LOCAL_FLOAT
        self.local_bool_count = LOCAL_BOOL
        self.local_char_count = LOCAL_CHAR
        # Temporales
        self.temp_int_count = TEMP_INT
        self.temp_float_count = TEMP_FLOAT
        self.temp_bool_count = TEMP_BOOL
        self.temp_char_count = TEMP_CHAR
        self.temp_pointer_count = TEMP_POINTER
        # Constantes
        self.const_int_count = CONST_INT
        self.const_float_count = CONST_FLOAT
        self.const_bool_count = CONST_BOOL
        self.const_char_count = CONST_CHAR
        # Constant Table
        self.constant_table = {} 
        # Stack of function calling
        self.func_call_stack = deque()
        # Used for constants in the meantime
        self.memory_table = {} 
        # For storing functions
        self.program_functions = {}

    def start_memory(self, func_dir):
        for func_name, func in func_dir.directory.items():
            memory_dict = {}
            vars = func['table'].table
            for var in vars.values():
                memory_dict[var['address']] = Memory(var['address'], get_default(type_to_char[var['type']]))
            params = {}
            if func_name != '0':
                func_params = func['params']
                for par in func_params:
                    # sample of par: ('int', 'p', 20000)
                    params[par[2]] = Memory(par[2], get_default(type_to_char[par[0]]))
            if func_name == "0":
                self.constant_table = {v.address: v for k, v in self.constant_table.items()}
                self.func_call_stack.append(FunctionMemory(func_name, memory_dict, params))
            else:
                self.program_functions[func_name] = FunctionMemory(func_name, memory_dict, params, func['start'])     
        

    def new_function_memory(self, func_id):
        temp_func = self.program_functions[func_id]
        temp_memory = temp_func.temp_memory.copy()
        temp_params = temp_func.params.copy()
        mem = {}
        params = {}
        for var in temp_memory.values():
            mem[var.address] = Memory(var.address, var.value)
        for par in temp_params.values():
            params[par.address] = Memory(par.address, par.value)

        func_mem = FunctionMemory(temp_func.func_name, mem, params, temp_func.start)
        return func_mem
    
    def get_new_global(self, t_type: str, increment: int = 1) -> int:
        if(t_type == "I"):
            current_next = self.global_int_count
            if (current_next + increment) > GLOBAL_FLOAT_LIMIT:
                raise Exception("ERROR: GLOBAL INT MEMORY EXCEEDED")
            self.global_int_count += increment
            return current_next
        elif (t_type == "F"):
            current_next = self.global_float_count
            if (current_next + increment) > GLOBAL_BOOL_LIMIT:
                raise Exception("ERROR: GLOBAL FLOAT MEMORY EXCEEDED")
            self.global_float_count += increment
            return current_next
        elif (t_type == "B"):
            current_next = self.global_bool_count
            if (current_next + increment) > GLOBAL_CHAR_LIMIT:
                raise Exception("ERROR: GLOBAL BOOL MEMORY EXCEEDED")
            self.global_bool_count += increment
            return current_next
        elif (t_type == "C"):
            current_next = self.global_char_count
            if (current_next + increment) > LOCAL_START:
                raise Exception("ERROR: GLOBAL CHAR MEMORY EXCEEDED")
            self.global_char_count += increment
            return current_next

    def get_new_local(self, t_type: str, increment: int = 1) -> int:
        if(t_type == "I"):
            current_next = self.local_int_count
            if (current_next + increment) > LOCAL_FLOAT_LIMIT:
                raise Exception("ERROR: LOCAL INT MEMORY EXCEEDED")
            self.local_int_count += increment
            return current_next
        elif (t_type == "F"):
            current_next = self.local_float_count
            if (current_next + increment) > LOCAL_BOOL_LIMIT:
                raise Exception("ERROR: LOCAL FLOAT MEMORY EXCEEDED")
            self.local_float_count += increment
            return current_next
        elif (t_type == "B"):
            current_next = self.local_bool_count
            if (current_next + increment) > LOCAL_CHAR_LIMIT:
                raise Exception("ERROR: LOCAL BOOL MEMORY EXCEEDED")
            self.local_bool_count += increment
            return current_next
        elif (t_type == "C"):
            current_next = self.local_char_count
            if (current_next + increment) > TEMP_START:
                raise Exception("ERROR: LOCAL CHAR MEMORY EXCEEDED")
            self.local_char_count += increment
            return current_next

    def get_new_temporal(self, t_type: str, increment: int = 1) -> int:
        if(t_type == "I"):
            current_next = self.temp_int_count
            if (current_next + increment) > TEMP_FLOAT_LIMIT:
                raise Exception("ERROR: TEMPORAL INT MEMORY EXCEEDED")
            self.temp_int_count += increment
            return current_next
        elif (t_type == "F"):
            current_next = self.temp_float_count
            if (current_next + increment) > TEMP_BOOL_LIMIT:
                raise Exception("ERROR: TEMPORAL FLOAT MEMORY EXCEEDED")
            self.temp_float_count += increment
            return current_next
        elif (t_type == "B"):
            current_next = self.temp_bool_count
            if (current_next + increment) > TEMP_CHAR_LIMIT:
                raise Exception("ERROR: TEMPORAL BOOL MEMORY EXCEEDED")
            self.temp_bool_count += increment
            return current_next
        elif (t_type == "C"):
            current_next = self.temp_char_count
            if (current_next + increment) > TEMP_POINTER_LIMIT:
                raise Exception("ERROR: TEMPORAL CHAR MEMORY EXCEEDED")
            self.temp_char_count += increment
            return current_next
        elif (t_type == "P"):
            current_next = self.temp_pointer_count
            if (current_next + increment) > CONST_START:
                raise Exception("ERROR: TEMPORAL POINTER MEMORY EXCEEDED")
            self.temp_pointer_count += increment
            return current_next

    def get_new_constant(self, t_type: str, increment: int = 1) -> int:
        if(t_type == "I"):
            current_next = self.const_int_count
            if (current_next + increment) > CONST_FLOAT_LIMIT:
                raise Exception("ERROR: CONSTANT INT MEMORY EXCEEDED")
            self.const_int_count += increment
            return current_next
        elif (t_type == "F"):
            current_next = self.const_float_count
            if (current_next + increment) > CONST_BOOL_LIMIT:
                raise Exception("ERROR: CONSTANT FLOAT MEMORY EXCEEDED")
            self.const_float_count += increment
            return current_next
        elif (t_type == "B"):
            current_next = self.const_bool_count
            if (current_next + increment) > CONST_CHAR_LIMIT:
                raise Exception("ERROR: CONSTANT BOOL MEMORY EXCEEDED")
            self.const_bool_count += increment
            return current_next
        elif (t_type == "C"):
            current_next = self.const_char_count
            if (current_next + increment) > CONST_LIMIT:
                raise Exception("ERROR: CONSTANT CHAR MEMORY EXCEEDED")
            self.const_char_count += increment
            return current_next

    # Regresa el conteo actual de variables locales y temporales
    def get_temps_and_locals(self) -> dict:
        count = {
            # Locales
            'LI': self.local_int_count - LOCAL_INT,
            'LF': self.local_float_count - LOCAL_FLOAT,
            'LB': self.local_bool_count - LOCAL_BOOL,
            'LC': self.local_char_count - LOCAL_CHAR,
            # Temporales
            'TI': self.temp_int_count - TEMP_INT,
            'TF': self.temp_float_count - TEMP_FLOAT,
            'TB': self.temp_bool_count - TEMP_BOOL,
            'TC': self.temp_char_count - TEMP_CHAR,
            'TP': self.temp_pointer_count - TEMP_POINTER,
        }
        return count

    # Resetea el conteo de variables locales y temporales
    def reset_temps_and_locals(self) -> None:
        # Locales
        self.local_int_count = LOCAL_INT
        self.local_float_count = LOCAL_FLOAT
        self.local_bool_count = LOCAL_BOOL
        self.local_char_count = LOCAL_CHAR
        # Temporales
        self.temp_int_count = TEMP_INT
        self.temp_float_count = TEMP_FLOAT
        self.temp_bool_count = TEMP_BOOL
        self.temp_char_count = TEMP_CHAR
        self.temp_pointer_count = TEMP_POINTER

    # Usar para tabla de tabla de constantes en un diccionario
    def get_constant_address(self, val: str, t_type: str, increment: int = 1) -> int:
        if str(val) in self.constant_table:
            return self.constant_table[str(val)].address
        address = self.get_new_constant(t_type, increment)
        new_v = Memory(address, val)
        self.constant_table[str(val)] = new_v
        self.memory_table[str(val)] = new_v
        return address

call_stack = deque()

def get_default(token):
    if token == 'I':
        return 0
    elif token == 'C':
        return ""
    elif token == 'F':
        return 0
    elif token == 'B':
        return True
