import argparse

from collections import deque
from lexer import LexerTudi
from memory import GLOBAL_START, LOCAL_START, TEMP_START, TEMP_POINTER, CONST_START, CONST_LIMIT, FunctionMemory, get_type_by_address
from parser_tudi import ParserTudi

class VirtualMachine():
    def __init__(self, input, verbose=False) -> None:
        # Init lexer
        self.lexer = LexerTudi()
        self.lexer.build()
        # Init parser
        self.parser = ParserTudi()
        self.parser.build(self.lexer, verbose)
        # Parse input
        self.parser.parse(input)

        # Retrieve information from parsing
        self.quadruples = self.parser.get_quadruples()
        self.func_dir = self.parser.get_function_directory()
        self.global_memory = self.func_dir.get_global_mem()
        self.const_table = self.parser.get_constant_table()
        self.counter = 0

        # Call stack
        self.curr_func = None
        self.func_call_stack = deque()

        # Goto stack
        self.goto_stack = deque()

    def start_machine(self):
        while self.counter < len(self.quadruples):
            self.do_action(self.quadruples[self.counter])
            self.counter += 1 # Going to next quadruple
    
    def do_action(self, quadruple):
        if quadruple.operator == '+':
            # --------------------------- SUMA ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand + right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '-':
            # --------------------------- RESTA ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand - right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '*':
            # --------------------------- MULTI ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand * right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '/':
            # --------------------------- DIV ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand / right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == 'y':
            # --------------------------- AND ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand and right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == 'o':
            # --------------------------- OR ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand or right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == 'no':
            # --------------------------- NOT ---------------------------
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = not right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '>=':
            # --------------------------- GE >= ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand >= right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '<=':
            # --------------------------- LE <= ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand <= right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '>':
            # --------------------------- GT > ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand > right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '<':
            # --------------------------- LT < ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand < right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '!=':
            # --------------------------- NE != ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand != right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '==':
            # --------------------------- EQ == ---------------------------
            left_operand = self.get_address_value(quadruple.left_operand)
            right_operand = self.get_address_value(quadruple.right_operand)
            temp_val = left_operand == right_operand
            self.set_address_value(quadruple.temp, temp_val)
        elif quadruple.operator == '=':
            # --------------------------- ASSIGNMENT ---------------------------
            length = quadruple.right_operand
            temp = quadruple.temp

            # Resultado es un pointer, entonces
            if TEMP_POINTER <= temp and temp < CONST_START:
                temp = self.curr_func.get_value_by_address(quadruple.temp)

            for i in range(length):
                temp_val = self.get_address_value(quadruple.left_operand + i)
                self.set_address_value(temp + i, temp_val)
        elif quadruple.operator == 'Read':
            quad_temp = quadruple.temp
            temp_val = input()
            # Resultado es un pointer, entonces
            if TEMP_POINTER <= quad_temp and quad_temp < CONST_START:
                quad_temp = self.curr_func.get_value_by_address(quad_temp)

            # Hacer cast correspondiente
            t_type = get_type_by_address(quad_temp)
            if t_type == 'I':
                temp_val = int(temp_val)
            elif t_type == 'F':
                temp_val = float(temp_val)
            elif t_type == 'B':
                temp_val = bool(temp_val)
            elif t_type == 'C':
                temp_val = temp_val[0]

            self.set_address_value(quad_temp, temp_val)
        elif quadruple.operator == 'Print':
            # --------------------------- PRINT ---------------------------
            try:
                print(self.get_address_value(quadruple.temp), end="", flush=True)
            except:
                temp = quadruple.temp.replace('\\n', '\n')
                print(temp.replace('"', ''), end="", flush=True)
        elif quadruple.operator == 'GOTO':
            # --------------------------- GOTO ---------------------------
            self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOTO_F':
            # --------------------------- GOTO_F ---------------------------
            if not self.get_address_value(quadruple.left_operand):
                self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOTO_V':
            # --------------------------- GOTO_V ---------------------------
            if self.get_address_value(quadruple.left_operand):
                self.counter = quadruple.temp - 2 # Go to this quad
        elif quadruple.operator == 'GOSUB':
            # --------------------------- GOSUB ---------------------------
            # Guardamos a donde hay que volver
            self.goto_stack.append(self.counter)
            # Seteamos la nueva función actual
            self.curr_func = self.func_call_stack[-1]
            # Nos vamos al inicio de la función
            self.counter = self.curr_func.start - 2
        elif quadruple.operator == 'ENDFUNC':
            if quadruple.temp is not None:
                raise Exception(f"Error: End of function reached without a returned value.")

            # Destruir funcion y regresar
            self.func_call_stack.pop()
            if len(self.func_call_stack) > 0:
                self.curr_func = self.func_call_stack[-1]
            else:
                self.curr_func = None

            self.counter = self.goto_stack.pop()
        elif quadruple.operator == 'ERA':
            # --------------------------- ERA ---------------------------
            # Agregamos al call stack
            func = self.func_dir.find_function(quadruple.temp)
            new_func = FunctionMemory(func["resources"], func["params"], func["start"], func["return_address"], func["return_type"][1][0])
            self.func_call_stack.append(new_func)
        elif quadruple.operator == 'PARAM':
            # --------------------------- PARAM ---------------------------
            # Obtenemos el número de parámetro - 1
            param_idx = int(quadruple.temp[3:]) - 1
            address = self.func_call_stack[-1].params_sequence[param_idx][2]
            length = self.func_call_stack[-1].params_sequence[param_idx][3][0]

            for i in range(length):
                left_operand = self.get_address_value(quadruple.left_operand + i)
                self.func_call_stack[-1].set_value_by_address(address + i, left_operand)
        elif quadruple.operator == 'RET':
            # --------------------------- RETURN ---------------------------
            # Obtenemos el número de parámetro - 1
            return_address = self.curr_func.return_address
            length = self.curr_func.return_length

            for i in range(length):
                return_value = self.get_address_value(quadruple.temp + i)
                self.set_address_value(return_address + i, return_value)

            self.func_call_stack.pop()
            if len(self.func_call_stack) > 0:
                self.curr_func = self.func_call_stack[-1]
            else:
                self.curr_func = None
            self.counter = self.goto_stack.pop()
        elif quadruple.operator == 'VER':
            # --------------------------- VERIFY BOUNDS ---------------------------
            index = self.get_address_value(quadruple.left_operand)
            upper_bound = self.get_address_value(quadruple.temp)
            # Checa que esté dentro del rango [0, upper_bound)
            if not (0 <= index and index < upper_bound):
                raise Exception(f"Index out of bounds")
        elif quadruple.operator == 'CAST':
            # --------------------------- CAST FUNCTIONS ---------------------------
            return_address = quadruple.right_operand
            try:
                temp = self.get_address_value(quadruple.temp)
            except:
                temp = quadruple.temp.replace('"', '')

            if quadruple.left_operand == 'int':
                value = int(temp)
                self.set_address_value(return_address, value)
            elif quadruple.left_operand == 'float':
                value = float(temp)
                self.set_address_value(return_address, value)
            elif quadruple.left_operand == 'bool':
                value = bool(temp)
                self.set_address_value(return_address, value)
        else:
            print("Not yet handled")

    def get_address_value(self, address):
        # Global
        if GLOBAL_START <= address and address < LOCAL_START:
            return self.global_memory[address]
        # Constantes
        if CONST_START <= address and address < CONST_LIMIT:
            return self.const_table[address]
        if TEMP_POINTER <= address and address < CONST_START:
            temp = self.curr_func.get_value_by_address(address)
            return self.get_address_value(temp)
        # Locals and temps
        if address >= LOCAL_START and address < CONST_START:
            return self.curr_func.get_value_by_address(address)

    def set_address_value(self, address, value):
        # Global
        if GLOBAL_START <= address and address < LOCAL_START:
            self.global_memory[address] = value
        # Locals and temps
        elif address >= LOCAL_START and address < CONST_START:
            self.curr_func.set_value_by_address(address, value)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="TUDI-VM", description="Virtual machine to parse and execute the TUDI programming language")
    parser.add_argument("filename", help="Filename with a TUDI program to parse and execute.")
    parser.add_argument("--verbose", action="store_true", help="Print all the details of the parsing phase.")
    args = parser.parse_args()

    f = open(args.filename, 'r')
    data = f.read()
    f.close()

    tudi = VirtualMachine(data, args.verbose)
    tudi.start_machine()