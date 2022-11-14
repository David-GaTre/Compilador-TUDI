from collections import deque #Para el stack de scopes


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
        return f'Adress: {self.address}, Value: {self.value}\n'

class FuncMemory():
    def __init__(self, function_name='', cont=-1, memory_list={}, params={}):
        self.function_name = function_name
        self.cont= cont
        self.prev = 0
        self.memory_list = memory_list.copy()
        self.params = params.copy()
    def __str__(self):
        return f'Function Name: {self.function_name}, Cont: {self.cont}, Memory List: {self.memory_list}, Params: {self.params}, Prev: {self.prev}\n'
    def __repr__(self):
        return f'Function Name: {self.function_name}, Cont: {self.cont}, Memory List: {self.memory_list}, Params: {self.params}, Prev: {self.prev}\n'


function_list = {} # This is used basically to store the functions generated in init_memory
memory_table = {} # It is used to store the constant values but with the key->address
constant_table= {} # It is used to store the constant values
call_stack = deque()

def init_memory(func_dir):
    global call_stack, param_counter
    for func_key in func_dir:
        func = func_dir[func_key]
        memory_list = {}
        params = {}
        current_vars = func.vars
        current_params = func.params
        param_counter = len(current_params) - 1
        for v in current_vars.values():
            if v.type == 'list':
                addr = v.address #we store the base address
                memory_list[v.address] = Memory(v.address,v.address, v.array_block)
                for i in range(0,memory_table[v.array_block.right].value):
                    # we generate the memory of the array with the default value
                    addr = addr + 1
                    memory_list[addr] = Memory(get_default_value(v.array_block.array_type), addr)
            else:
                memory_list[v.address] = Memory(get_default_value(v.type),v.address)
        for p in current_params:
            params[param_counter] = Memory(get_default_value(p.type),p.address)
            param_counter-=1
        function_list[func_key] = FuncMemory(func_key,func.cont, memory_list,params)     
        if func_key == "global":
            call_stack.append(FuncMemory(func_key,func.cont, memory_list,params))

def get_default_value(token):
    if token == 'I':
        return 0
    elif token == 'C':
        return ""
    elif token == 'F':
        return 0
    elif token == 'B':
        return True

def get_const_address(value, type):
    if value in constant_table.keys():
        return constant_table[value].address
    address = get_next_constant(type)
    new_value = Memory(value, address)
    constant_table[value] = new_value
    memory_table[address] = new_value
    return address

def get_next_global_value(token):
    if(token == "I"):
        global GLOBAL_INT
        GLOBAL_INT += 1
        if GLOBAL_INT >= GLOBAL_FLOAT_LIMIT:
            raise Exception("ERROR: GLOBAL INT MEMORY EXCEEDED")
        return GLOBAL_INT
    
    elif (token == "F"):
        global GLOBAL_FLOAT
        GLOBAL_FLOAT += 1
        if GLOBAL_FLOAT >= GLOBAL_BOOL_LIMIT:
            raise Exception("ERROR: GLOBAL FLOAT MEMORY EXCEEDED")

        return GLOBAL_FLOAT 
    elif (token == "B"):
        global GLOBAL_BOOL
        GLOBAL_BOOL += 1
        if GLOBAL_BOOL >= GLOBAL_CHAR_LIMIT:
            raise Exception("ERROR: GLOBAL BOOL MEMORY EXCEEDED")
        return GLOBAL_BOOL
    elif (token == "C"):
        global GLOBAL_CHAR
        GLOBAL_CHAR += 1
        if GLOBAL_CHAR >= LOCAL_START:
            raise Exception("ERROR: GLOBAL CHAR MEMORY EXCEEDED")
        return GLOBAL_CHAR
        
# Gets the next local
def get_next_local(token):
    if(token == "I"):
        global LOCAL_INT
        LOCAL_INT += 1
        if LOCAL_INT >= LOCAL_FLOAT_LIMIT:
            raise Exception("ERROR: LOCAL INT MEMORY EXCEEDED") 
        return LOCAL_INT
    elif (token == "F"):
        global LOCAL_FLOAT
        LOCAL_FLOAT += 1
        if LOCAL_FLOAT >= LOCAL_BOOL_LIMIT:
            raise Exception("ERROR: LOCAL FLOAT MEMORY EXCEEDED") 
        return LOCAL_FLOAT 
    elif (token == "B"):
        global LOCAL_BOOL
        LOCAL_BOOL += 1
        if LOCAL_BOOL >= LOCAL_CHAR_LIMIT:
            raise Exception("ERROR: LOCAL BOOL MEMORY EXCEEDED") 
        return LOCAL_BOOL
    elif (token == "C"):
        global LOCAL_CHAR
        LOCAL_CHAR += 1
        if LOCAL_CHAR >= TEMP_START:
            raise Exception("ERROR: LOCAL CHAR MEMORY EXCEEDED") 
        return LOCAL_CHAR
        
def get_next_temporal(token):
    if(token == "I"):
        global TEMP_INT
        TEMP_INT += 1
        if TEMP_INT >= TEMP_FLOAT_LIMIT:
            raise Exception("ERROR: TEMPORAL INT MEMORY EXCEEDED") 
        return TEMP_INT
    elif (token == "F"):
        global TEMP_FLOAT
        TEMP_FLOAT += 1
        if TEMP_FLOAT >= TEMP_BOOL_LIMIT:
            raise Exception("ERROR: TEMPORAL FLOAT MEMORY EXCEEDED") 
        return TEMP_FLOAT 
    elif (token == "B"):
        global TEMP_BOOL
        TEMP_BOOL += 1
        if TEMP_BOOL >= TEMP_CHAR_LIMIT:
            raise Exception("ERROR: TEMPORAL BOOL MEMORY EXCEEDED") 
        return TEMP_BOOL
    elif (token == "C"):
        global TEMP_CHAR
        TEMP_CHAR += 1
        if TEMP_CHAR >= CONST_START:
            raise Exception("ERROR: TEMPORAL CHAR MEMORY EXCEEDED") 
        return TEMP_CHAR
        
# Get next constant
def get_next_constant(token):
    if(token == "I"):
        global CONST_INT
        CONST_INT += 1
        if CONST_INT >= CONST_FLOAT_LIMIT:
            raise Exception("ERROR: CONSTANT INT MEMORY EXCEEDED") 
        return CONST_INT
    elif (token == "F"):
        global CONST_FLOAT
        CONST_FLOAT += 1
        if CONST_FLOAT >= CONST_BOOL_LIMIT:
            raise Exception("ERROR: CONSTANT FLOAT MEMORY EXCEEDED") 
        return CONST_FLOAT 
    elif (token == "B"):
        global CONST_BOOL
        CONST_BOOL += 1
        if CONST_BOOL >= CONST_CHAR_LIMIT:
            raise Exception("ERROR: CONSTANT BOOL MEMORY EXCEEDED") 
        return CONST_BOOL
    elif (token == "C"):
        global CONST_CHAR
        CONST_CHAR += 1
        if CONST_CHAR >= CONST_LIMIT:
            raise Exception("ERROR: CONSTANT CHAR MEMORY EXCEEDED") 
        return CONST_CHAR
