from lexer import LexerTudi, Token
from dir_vars import FunctionsDirectory
from collections import deque
from sem_cube import SemanticCube

import ply.yacc as yacc


class Quadruple():
    def __init__(self, operator, left_operand, right_operand, temp):
        global count_q
        self.id = count_q
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.temp = temp
        count_q += 1

    def __str__(self):
        return f'id: {self.id}, operator: {self.operator}, left_operand: {self.left_operand}, right_operand: {self.right_operand}, temp: {self.temp}\n'

quadruples = []
operator_stack = deque() 
operand_stack = deque() 
type_stack = deque() 
goto_stack = deque() 
sem_cube = SemanticCube()
count_q = 1
arr_relops = ['<', '<=', '==', '>', '>=', '!=']
arr_logicops = ['y', 'o']
type_dict = {'int': 'I', 'float': 'F', 'char': 'C', 'bool': 'B', 'arr1d': 'A'}
temp_vars = 0

def get_next_temp():
    # On the meantime returns string, wait for memory implementation
    global temp_vars
    temp_vars +=1
    return 'T' + str(temp_vars)

def check_stack_operand(arr_operands):
    if len(operator_stack) > 0 and (operator_stack[-1] in arr_operands):
        right_oper = operand_stack.pop()
        left_oper = operand_stack.pop()
        right_type = type_stack.pop()
        left_type = type_stack.pop()
        operator = operator_stack.pop()
        result_t = sem_cube.validate_expression(left_type, right_type, operator)

        if result_t == "ERROR: Not valid operation":
            raise Exception("TYPE MISMATCH")
        t = get_next_temp()
        quadruples.append(Quadruple(operator, left_oper, right_oper, t))
        operand_stack.append(t)
        result_t = type_dict[result_t]
        type_stack.append(result_t)

class ParserTudi(object):

    tokens = LexerTudi.tokens
    literals = LexerTudi.literals

    def p_game(self, p):
        '''game : GAME ID ';' CANVAS ASSIGN_OP INT_LITERAL ',' INT_LITERAL ';' game_vars game_funcs'''
        p[0] = "Aceptado"
        print("Todo valido")

        for func, func_items in self.func_dir.directory.items():
            print('Scope:', func)
            for func_item, values in func_items.items():
                if func_item == 'table':
                    print('\t- Variables:')
                    for k, v  in values.table.items():
                        print('\t---', k, v)
                else:
                    print('\t-', func_item, ':', values)
            print()
        for i in quadruples:
            print(i)

    def p_game_vars(self, p):
        '''game_vars : block_vars
                    | empty'''

    def p_game_funcs(self, p):
        '''game_funcs : declare_func game_funcs
                    | game_start'''

    def p_game_start(self, p):
        '''game_start : func_start game_update
                    | game_update'''

    def p_game_update(self, p):
        '''game_update : func_update
                    | empty'''

    def p_block_vars(self, p):
        '''block_vars : DECLARE '{' declare_vars '}' '''

    def p_declare_vars(self, p):
        '''declare_vars : declare_var declare_vars
                        | empty'''

    def p_declare_var(self, p):
        '''declare_var : type list_vars ';' '''
        self.last_vars['var_type'] = p[1]

        for var_id in p[2]:
            if not self.func_dir.add_variable(self.last_vars['scope'], var_id.value, self.last_vars['var_type']):
                print(f'Error: Re-declaration of variable \'{var_id.value}\' at line: {var_id.lineno}')
                exit()

    def p_list_vars(self, p):
        '''list_vars : ID list_vars_prima'''
        p[0] = [Token(p[1], p.lineno(1))] + p[2]

    def p_list_vars_prima(self, p):
        '''list_vars_prima : ',' ID list_vars_prima
                        | empty'''
        if len(p) > 2:
            p[0] = [Token(p[2], p.lineno(2))] + p[3]
        else:
            p[0] = []

    def p_declare_func(self, p):
        '''declare_func : FUNC ID ':' func_type seen_dec_func '(' list_params ')' '{' block_code '}' '''

    def p_func_start(self, p):
        '''func_start : FUNC START ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

    def p_func_update(self, p):
        '''func_update : FUNC UPDATE ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

    def p_list_params(self, p):
        '''list_params : type ID seen_param list_params_prima
                    | empty'''

    def p_list_params_prima(self, p):
        '''list_params_prima : ',' type ID seen_param list_params_prima
                            | empty'''

    def p_func_type(self, p):
        '''func_type : type
                    | VOID '''
        p[0] = p[1]

    def p_block_code(self, p):
        '''block_code : block_vars statement_prima
                    | statement statement_prima
                    | empty'''

    def p_statement(self, p):
        '''statement : call_func ';'
                    | for_loop
                    | while_loop
                    | conditional
                    | assignment ';'
                    | return ';'
                    | call_method ';' '''

    def p_statement_prima(self, p):
        '''statement_prima : statement statement_prima
                        | empty'''

    def p_return(self, p):
        '''return : RETURN god_exp'''

    def p_io_func(self, p):
        '''io_func : PRINT '(' io_func_prima ')'
                | READ  '(' io_func_prima ')' '''

    def p_io_func_prima(self, p):
        '''io_func_prima : STRING_LITERAL
                        | empty'''

    def p_cast_func(self, p):
        '''cast_func : INT cast_func_prima
                    | FLOAT cast_func_prima
                    | BOOLEAN cast_func_prima'''

    def p_cast_func_prima(self, p):
        '''cast_func_prima : '(' STRING_LITERAL ')'
                        | '(' god_exp ')' '''

    def p_call_func(self, p):
        '''call_func : ID '(' list_args ')'
                    | io_func
                    | cast_func'''
        if len(p) > 2:
            if not self.func_dir.find_function(p[1]):
                print(f'Error: Function \'{p[1]}\' at line {p.lineno(1)} was not declared.')
                exit()
        p[0] = [0, 'B', p[0]] # Dummy value in the meantime, need help obtaining data type

    def p_call_method(self, p):
        '''call_method : id_exp '.' call_method_prima '(' list_args ')' '''

    def p_call_method_prima(self, p):
        '''call_method_prima : SETPOSITION
                            | TRANSLATE
                            | SETCONTROLLABLE '''

    def p_list_args(self, p):
        '''list_args : god_exp list_args_prima
                    | empty'''

    def p_list_args_prima(self, p):
        '''list_args_prima : ',' god_exp list_args_prima
                        | empty'''

    def p_for_loop(self, p):
        '''for_loop : FOR '(' assignment ';' god_exp ';' assignment ')' '{' block_code '}' '''

    def p_while_loop(self, p):
        '''while_loop : WHILE while_act_1 '(' god_exp ')' '{' block_code '}' '''

    def p_while_act_1(self, p):
        '''while_act_1 : '''
        goto_stack.append(len(quadruples))

    def p_conditional(self, p):
        '''conditional : IF '(' god_exp ')' '{' block_code '}' conditional_prima'''

    def p_conditional_prima(self, p):
        '''conditional_prima : ELSE conditional
                            | ELSE '{' block_code '}'
                            | empty'''

    def p_assignment(self, p):
        '''assignment : id_exp ASSIGN_OP god_exp'''

    def p_type(self, p):
        '''type : INT type_dims
                | FLOAT type_dims
                | BOOLEAN type_dims
                | CHAR type_dims
                | SPRITE type_dims'''
        if p[2] is not None:
            p[0] = "-".join([p[1], p[2]])
        else:
            p[0] = p[1]

    def p_type_dims(self, p):
        '''type_dims : '[' INT_LITERAL ']'
                    | '[' INT_LITERAL ',' INT_LITERAL ']'
                    | empty'''
        if len(p) == 6:
            p[0] = 'arr2d'
        elif len(p) == 4:
            p[0] = 'arr1d'


    def p_god_exp(self, p):
        '''god_exp : super_exp god_exp_neuro_1 god_exp_prima'''

    def p_god_exp_neuro_1(self, p):
        '''god_exp_neuro_1 : '''
        check_stack_operand(arr_logicops)

    def p_god_exp_prima(self, p):
        '''god_exp_prima : LOGIC_OPS add_op god_exp
                        | empty'''

    def p_super_exp(self, p):
        '''super_exp : exp super_exp_neuro_1 super_exp_prima'''

    def p_super_exp_neuro_1(self, p):
        '''super_exp_neuro_1 : '''
        check_stack_operand(arr_relops)

    def p_super_exp_prima(self, p):
        '''super_exp_prima : REL_OPS add_op exp
                        | empty'''

    def p_exp(self, p):
        '''exp : term exp_neuro_1 exp_prima'''

    def p_exp_neuro_1(self, p):
        '''exp_neuro_1 : '''
        check_stack_operand(["+", "-"])

    def p_exp_prima(self, p):
        '''exp_prima : '+' add_op exp
                    | '-' add_op exp
                    | empty'''

    def p_term(self, p):
        '''term : fact term_neuro_1 term_prima'''

    def p_term_neuro_1(self, p):
        '''term_neuro_1 : '''
        check_stack_operand(["*", "/"])

    def p_term_prima(self, p):
        '''term_prima : '/' add_op term
                    | '*' add_op term
                    | empty'''

    def p_fact(self, p):
        '''fact : fact_neuro_1 '(' god_exp ')' fact_neuro_2
                | fact_constants '''

        if len(p) == 2:
            operand_stack.append(p[1][0]) # aiuda
            type_stack.append(p[1][1]) # aiuda
        p[0] = p[1]


    def p_fact_constants(self, p):
        '''
        fact_constants : id_exp
                        | int
                        | float
                        | bool
                        | call_func
        '''
        p[0] = p[1]

    def p_int(self, p):
        '''int : INT_LITERAL'''
        p[0] = [p[1], 'I'] # Dummy value on the meantime

    def p_float(self, p):
        '''float : FLOAT_LITERAL'''
        p[0] = [p[1], 'F'] # Dummy value on the meantime

    def p_bool(self, p):
        '''bool : BOOL_LITERAL'''
        p[0] = [p[1], 'B'] # Dummy value on the meantime

    def p_add_op(self, p):
        '''add_op : '''
        operator_stack.append(p[-1]) # Add previous operator to stack

    def p_fact_neuro_1(self, p):
        '''fact_neuro_1 :'''
        operator_stack.append("|") # Fondo falso

    def p_fact_neuro_2(self, p):
        '''fact_neuro_2 :'''
        operator_stack.pop() # Fin del fondo falso

    def p_id_exp(self, p):
        '''id_exp : id_term
                | id_term '[' god_exp ']'
                | id_term '[' god_exp ',' god_exp ']' '''
        if len(p) == 6:
            p[0] = Token([p[1][0], p[3], p[5]], p.lineno(1))
        elif len(p) == 4:
            p[0] = Token([p[1][0], p[3]], p.lineno(1))
        else:
            p[0] = Token(p[1][0], p.lineno(1))

        if not self.func_dir.find_variable(self.last_vars['scope'], p[1][0]):
            print(f'Error: Variable \'{p[1]}\' at line {p.lineno(1)} was not declared.')
            exit()
        p[0] = [0, p[1][1], p[0]]

    def p_id_term(self, p):
        '''id_term : ID'''
        p[0] = [p[1], 'B'] # need help obtaining the type of the variable

    def p_seen_dec_func(self, p):
        '''seen_dec_func :'''
        # Al llegar a esta regla, significa que hemos visto el inicio de
        # la declaración de una función.
        # p[-1] es la producción en la que aparece el tipo de retorno
        # p[-3] es la producción en la que aparece el nombre de la función
        self.last_vars['scope'] = p[-3]
        if not self.func_dir.add_function(self.last_vars['scope'], p[-1]):
            print(f'Error: Re-declaration of function \'{p[-3]}\'.')
            exit()

    def p_seen_param(self, p):
        '''seen_param :'''
        # Al llegar a esta regla, significa que hemos visto
        # la declaración de un parámetro.
        # p[-1] es la producción en la que aparece nombre del parámetro
        # p[-2] es la producción en la que aparece el tipo de dato
        if not self.func_dir.add_param(self.last_vars['scope'], p[-1], p[-2]):
            print(f'Error: Re-declaration of function parameter \'{p[-1]}\'.')
            exit()

    def p_empty(self, p): # representa epsilon
        '''empty : '''
        pass

    def p_error(self, p):
        print("Syntax error in input at line: ", p, p.lineno)
        exit()

    def build(self, lexer, **kwargs):
        self.func_dir = FunctionsDirectory()
        self.last_vars = {'scope': self.func_dir.GLOBAL_ENV, 'var_type': None}

        self.lexer = lexer
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data)
