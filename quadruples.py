from collections import deque

type_dict = {'int': 'I', 'float': 'F', 'char': 'C', 'bool': 'B', 'arr1d': 'A', 'sprite': 'S'}

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

    def get_next_temp(self):
        # On the meantime returns string, wait for memory implementation
        self.temp_vars += 1
        return 'T' + str(self.temp_vars)

    # Utiliza un cubo semántico para validar que una expresión es correcta
    def check_stack_operand(self, arr_operators, sem_cube):
        if len(self.operator_stack) > 0 and (self.operator_stack[-1] in arr_operators):
            right_oper = self.operand_stack.pop()
            right_type = self.type_stack.pop()
            
            left_oper = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            operator = self.operator_stack.pop()

            result_t = sem_cube.validate_expression(left_type, right_type, operator)

            if result_t == "ERROR: Not valid operation":
                raise Exception("TYPE MISMATCH")

            t = self.get_next_temp()
            
            self.quadruples.append(Quadruple(self.count_q, operator, left_oper, right_oper, t))
            self.count_q += 1
            
            result_t = type_dict[result_t]
            self.operand_stack.append(t)
            self.type_stack.append(result_t)

    def finish_expression(self, sem_cube):
        while len(self.operator_stack) > 0 and self.operator_stack[-1] != "|":
            right_oper = self.operand_stack.pop()
            right_type = self.type_stack.pop()

            left_oper = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            operator = self.operator_stack.pop()

            result_t = sem_cube.validate_expression(left_type, right_type, operator)

            if result_t == "ERROR: Not valid operation":
                raise Exception("TYPE MISMATCH")

            t = self.get_next_temp()

            self.quadruples.append(Quadruple(self.count_q, operator, left_oper, right_oper, t))
            self.count_q += 1

            result_t = type_dict[result_t]
            self.operand_stack.append(t)
            self.type_stack.append(result_t)

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
