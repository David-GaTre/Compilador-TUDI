from collections import deque

type_to_char = {'int': 'I', 'float': 'F', 'char': 'C', 'bool': 'B', 'unary': 'U', 'void': 'V'}
char_to_type = {'I': 'int', 'F': 'float', 'C': 'char', 'B': 'bool', 'U': 'unary', 'V': 'void'}

class QuadrupleGenerator():
    def __init__(self):
        # Cuadruplos y contador
        self.quadruples = []
        self.count_q = 1
        
        # Variables temporales
        self.temp_vars = 0
        
        # Pilas
        self.operator_stack = deque() 
        self.operand_stack = deque() 
        self.type_stack = deque() 
        self.goto_stack = deque()
        self.params_stack = deque()

    # Añade una operador a la pila correspondiente
    def add_operator(self, operator):
        self.operator_stack.append(operator)

    # Regresa y elimina el operador más reciente en la pila correspondiente
    def pop_operator(self):
        return self.operator_stack.pop()

    # Añade un tipo y operando a las pila correspondientes
    def add_operand(self, type_t, operand):
        self.type_stack.append(type_t)
        self.operand_stack.append(operand)

    def add_quad_from_parser(self, operator, left_operand, right_operand, temp):
        self.quadruples.append(Quadruple(self.count_q, operator, left_operand, right_operand, temp))
        self.count_q += 1 

    # Regresa y elimina el tipo y operando más recientes de las pilas correspondientes
    def pop_operand(self):
        return self.type_stack.pop(), self.operand_stack.pop()

    # Utiliza un cubo semántico para validar que una expresión es correcta
    def check_stack_operand(self, arr_operators, sem_cube, virtual_mem):
        if len(self.operator_stack) > 0 and (self.operator_stack[-1] in arr_operators):
            right_oper = self.operand_stack.pop()
            right_type = self.type_stack.pop()
            
            left_oper = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            operator = self.operator_stack.pop()

            result_t = sem_cube.validate_expression(left_type, right_type, operator)

            if result_t == "ERROR: Not valid operation":
                raise Exception(f"TYPE MISMATCH: {left_oper} ({char_to_type[left_type]}) {operator} {right_oper} ({char_to_type[right_type]})")

            t = virtual_mem.get_new_temporal(type_to_char[result_t])
            
            self.quadruples.append(Quadruple(self.count_q, operator, left_oper, right_oper, t))
            self.count_q += 1
            
            result_t = type_to_char[result_t]
            self.operand_stack.append(t)
            self.type_stack.append(result_t)

    def finish_expression(self, sem_cube, virtual_mem):
        while len(self.operator_stack) > 0 and self.operator_stack[-1] != "|":
            right_oper = self.operand_stack.pop()
            right_type = self.type_stack.pop()

            left_oper = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            operator = self.operator_stack.pop()

            result_t = sem_cube.validate_expression(left_type, right_type, operator)

            if result_t == "ERROR: Not valid operation":
                raise Exception("TYPE MISMATCH")

            t = virtual_mem.get_new_temporal(type_to_char[result_t])

            self.quadruples.append(Quadruple(self.count_q, operator, left_oper, right_oper, t))
            self.count_q += 1

            result_t = type_to_char[result_t]
            self.operand_stack.append(t)
            self.type_stack.append(result_t)

    def add_assignment(self, var_id, var_val, length=1):
        self.quadruples.append(Quadruple(self.count_q, '=', var_val, length, var_id))
        self.count_q += 1

    def print_quadruples(self):
        for i in self.quadruples:
            print(i)

class Quadruple():
    def __init__(self, id, operator, left_operand, right_operand, temp):
        self.id = id
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.temp = temp

    def __str__(self):
        return f'{self.id}: [{self.operator}, {self.left_operand}, {self.right_operand}, {self.temp}]'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Quadruple):
            return False
        return self.__str__() == other.__str__()
