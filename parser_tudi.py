from lexer import LexerTudi, Token
from dir_vars import FunctionsDirectory
from sem_cube import SemanticCube
from quadruples import QuadrupleGenerator

import ply.yacc as yacc

sem_cube = SemanticCube()

arr_relops = ['<', '<=', '==', '>', '>=', '!=']
arr_logicops = ['y', 'o']

class ParserTudi(object):
    # Character literals y tokens necesarios para que el parser
    # los conozca y los pueda interpretar en sus reglas
    tokens = LexerTudi.tokens
    literals = LexerTudi.literals

    # Estructura general de un programa en TUDI:
    # - Inicia con un ID para el nombre del juego
    # - Asigna el tamaño (width, height) al canvas
    # - Declaración de variables globales
    # - Definición de funciones
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

        self.quadruple_gen.print_quadruples()

    # Declaración de variables globales (opcional)
    def p_game_vars(self, p):
        '''game_vars : block_vars
                     | empty'''

    # Definición de funciones:
    # - Funciones definidas por el usuario (opcionales)
    # - Llenar funciones Start y Update de TUDI (opcionales)
    #   con código del usuario
    def p_game_funcs(self, p):
        '''game_funcs : declare_func game_funcs
                      | game_start'''

    # Definición de función Start de TUDI (opcional)
    # Continúa con función Update de TUDI
    def p_game_start(self, p):
        '''game_start : func_start game_update
                      | game_update'''

    # Definición de función Update de TUDI (opcional)
    def p_game_update(self, p):
        '''game_update : func_update
                       | empty'''

    # Bloque de declaración de variables
    def p_block_vars(self, p):
        '''block_vars : DECLARE '{' declare_vars '}' '''

    # Declaración de variables (permite múltiples declaraciones)
    def p_declare_vars(self, p):
        '''declare_vars : declare_var declare_vars
                        | empty'''

    # Declara 1 o más variables de un tipo de dato en común
    def p_declare_var(self, p):
        '''declare_var : type list_vars ';' '''
        self.last_vars['var_type'] = p[1]

        # Checar por nombres de variables duplicadas en el scope actual
        for var_id in p[2]:
            if not self.func_dir.add_variable(self.last_vars['scope'], var_id.value, self.last_vars['var_type']):
                print(f'Error: Re-declaration of variable \'{var_id.value}\' at line: {var_id.lineno}')
                raise Exception(f'Error: Re-declaration of variable \'{var_id.value}\' at line: {var_id.lineno}')

    # Lista de variables
    def p_list_vars(self, p):
        '''list_vars : ID list_vars_prima'''
        p[0] = [Token(p[1], p.lineno(1))] + p[2]

    # Añadir una variable a la lista de variables
    def p_list_vars_prima(self, p):
        '''list_vars_prima : ',' ID list_vars_prima
                           | empty'''
        if len(p) > 2:
            p[0] = [Token(p[2], p.lineno(2))] + p[3]
        else:
            p[0] = []

    # Función definida por el usuario, necesita de:
    # - Un tipo de retorno
    # - Una lista de parámetros
    # - Código de la función
    def p_declare_func(self, p):
        '''declare_func : FUNC ID ':' func_type seen_dec_func '(' list_params ')' '{' block_code '}' '''

    # Definición de función Start de TUDI:
    # - Si está presente en el programa, la función Start es
    #   la primera en ejecutarse
    def p_func_start(self, p):
        '''func_start : FUNC START ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

    # Definición de función Update de TUDI:
    # - Si está presente en el programa, la función Update es
    #   la función que está siendo ejecutada constantemente (loop)
    def p_func_update(self, p):
        '''func_update : FUNC UPDATE ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

    # Lista de parámetros de una función
    def p_list_params(self, p):
        '''list_params : type ID seen_param list_params_prima
                       | empty'''

    # Añadir un parámetro a la lista de parámetros
    def p_list_params_prima(self, p):
        '''list_params_prima : ',' type ID seen_param list_params_prima
                             | empty'''

    # Tipo de dato posible como retorno de una función:
    # - Todos y VOID
    def p_func_type(self, p):
        '''func_type : type
                     | VOID '''
        p[0] = p[1]

    # Bloque de código, puede incluir:
    # - Bloque de declaración de variables
    # - Estatutos
    def p_block_code(self, p):
        '''block_code : block_vars statement_prima
                      | statement statement_prima
                      | empty'''

    # Un estatuto puede ser:
    # - Llamada a una función o métodos
    # - Ciclos o condicionales
    # - Asignaciones
    # - Estatuto de retorno
    def p_statement(self, p):
        '''statement : call_func ';'
                     | for_loop
                     | while_loop
                     | conditional
                     | assignment ';'
                     | return ';'
                     | call_method ';' '''

    # Añadir un estatuto más
    def p_statement_prima(self, p):
        '''statement_prima : statement statement_prima
                           | empty'''

    # Estatuto de retorno:
    # - Regresa una expresión
    def p_return(self, p):
        '''return : RETURN god_exp'''

    # Funciones built-in de I/O en TUDI:
    # - Print: Muestra en consola el argumento provisto
    # - Read: Pide input del usuario, como prompt utiliza
    #         el argumento provisto. Retorna un string literal
    def p_io_func(self, p):
        '''io_func : PRINT '(' io_func_prima ')'
                   | READ  '(' io_func_prima ')' '''

    # El argumento posible de una función I/O
    def p_io_func_prima(self, p):
        '''io_func_prima : STRING_LITERAL
                         | empty'''

    # Funciones built-in de cast en TUDI:
    # - Para los tipos de datos: int, float y bool
    # - Reciben un string literal o un arreglo de chars
    def p_cast_func(self, p):
        '''cast_func : INT cast_func_prima
                     | FLOAT cast_func_prima
                     | BOOLEAN cast_func_prima'''

    # El argumento posible de una función de cast:
    # - String literal o arreglo de chars
    def p_cast_func_prima(self, p):
        '''cast_func_prima : '(' STRING_LITERAL ')'
                           | '(' god_exp ')' '''

    # Llamada a una función
    def p_call_func(self, p):
        '''call_func : ID '(' list_args ')'
                     | io_func
                     | cast_func'''
        # Checa que exista una función definida por el usuario
        if len(p) > 2:
            if not self.func_dir.find_function(p[1]):
                print(f'Error: Function \'{p[1]}\' at line {p.lineno(1)} was not declared.')
                raise Exception(f'Error: Function \'{p[1]}\' at line {p.lineno(1)} was not declared.')
        p[0] = [0, 'B', p[0]] # Dummy value in the meantime, need help obtaining data type

    # Llamada a un método, requisitos:
    # - Los únicos métodos en TUDI pertenecen a una variable de tipo sprite
    def p_call_method(self, p):
        '''call_method : id_exp '.' call_method_prima '(' list_args ')' '''

    # Los métodos built-in en TUDI para el tipo de dato sprite:
    # - SetPosition: Recibe dos floats,
    #                correspondientes a las coordenadas (x, y)
    # - Translate: Recibe dos floats,
    #              desplaza el sprite en las dos dimensiones
    # - SetControllable: Recibe un bool,
    #                    define si el sprite puede ser manipulado por las teclas del usuario
    def p_call_method_prima(self, p):
        '''call_method_prima : SETPOSITION
                             | TRANSLATE
                             | SETCONTROLLABLE '''

    # Lista de argumentos (expresiones)
    def p_list_args(self, p):
        '''list_args : god_exp list_args_prima
                     | empty'''

    # Añadir un argumento a la lista de argumentos
    def p_list_args_prima(self, p):
        '''list_args_prima : ',' god_exp list_args_prima
                           | empty'''

    # Ciclo for loop (C/C++ style)
    def p_for_loop(self, p):
        '''for_loop : FOR '(' assignment ';' god_exp ';' assignment ')' '{' block_code '}' '''

    # Ciclo while clásico (C/C++ style)
    def p_while_loop(self, p):
        '''while_loop : WHILE while_act_1 '(' god_exp ')' '{' block_code '}' '''

    def p_while_act_1(self, p):
        '''while_act_1 : '''
        # goto_stack.append(len(quadruples)

    # If condicional (C/C++ style)
    def p_conditional(self, p):
        '''conditional : IF '(' god_exp ')' '{' block_code '}' conditional_prima'''

    # Else-If / Else condicional (C/C++ style)
    def p_conditional_prima(self, p):
        '''conditional_prima : ELSE conditional
                             | ELSE '{' block_code '}'
                             | empty'''

    # Asignación de una expresión a una variables:
    # - Se debe verificar que los tipos de datos coincidan
    def p_assignment(self, p):
        '''assignment : id_exp ASSIGN_OP god_exp'''

    # Tipos de datos en TUDI:
    # - Pueden ser arreglos de 1 o 2 dimensiones
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

    # En la declaración, los arreglos solamente
    # aceptan int literals para la definición del tamaño
    def p_type_dims(self, p):
        '''type_dims : '[' INT_LITERAL ']'
                     | '[' INT_LITERAL ',' INT_LITERAL ']'
                     | empty'''
        if len(p) == 6:
            p[0] = 'arr2d'
        elif len(p) == 4:
            p[0] = 'arr1d'

    # Expresión (lógica, relacional, aritmética)
    def p_god_exp(self, p):
        '''god_exp : super_exp god_exp_neuro_1 god_exp_prima'''

    def p_god_exp_neuro_1(self, p):
        '''god_exp_neuro_1 : '''
        self.quadruple_gen.check_stack_operand(arr_logicops, sem_cube)

    # Operadores lógicos
    def p_god_exp_prima(self, p):
        '''god_exp_prima : LOGIC_OPS add_op god_exp
                         | empty'''

    def p_super_exp(self, p):
        '''super_exp : exp super_exp_neuro_1 super_exp_prima'''

    def p_super_exp_neuro_1(self, p):
        '''super_exp_neuro_1 : '''
        self.quadruple_gen.check_stack_operand(arr_relops, sem_cube)

    # Operadores relacionales
    def p_super_exp_prima(self, p):
        '''super_exp_prima : REL_OPS add_op exp
                           | empty'''

    def p_exp(self, p):
        '''exp : term exp_neuro_1 exp_prima'''

    def p_exp_neuro_1(self, p):
        '''exp_neuro_1 : '''
        self.quadruple_gen.check_stack_operand(["+", "-"], sem_cube)

    # Operadores suma y resta
    def p_exp_prima(self, p):
        '''exp_prima : '+' add_op exp
                     | '-' add_op exp
                     | empty'''

    def p_term(self, p):
        '''term : fact term_neuro_1 term_prima'''

    def p_term_neuro_1(self, p):
        '''term_neuro_1 : '''
        self.quadruple_gen.check_stack_operand(["*", "/"], sem_cube)

    # Operadores de multiplación y división
    def p_term_prima(self, p):
        '''term_prima : '/' add_op term
                      | '*' add_op term
                      | empty'''

    # Factores de una expresión:
    # - Operadores de agrupacion (paréntesis)
    # - Variables y literals
    # - Llamadas a una función (lo que retorna)
    def p_fact(self, p):
        '''fact : '(' fact_neuro_1 god_exp ')' fact_neuro_2
                | fact_constants '''

        if len(p) == 2:
            # (Type, operand)
            self.quadruple_gen.add_operand(p[1][1], p[1][0])
        p[0] = p[1]

    # Variables, literals, y llamadas a una función
    def p_fact_constants(self, p):
        '''
        fact_constants : id_exp
                       | int
                       | float
                       | bool
                       | call_func
        '''
        p[0] = p[1]

    # Enteros
    def p_int(self, p):
        '''int : INT_LITERAL'''
        p[0] = [p[1], 'I'] # Dummy value on the meantime

    # Flotantes
    def p_float(self, p):
        '''float : FLOAT_LITERAL'''
        p[0] = [p[1], 'F'] # Dummy value on the meantime

    # Booleanos
    def p_bool(self, p):
        '''bool : BOOL_LITERAL'''
        p[0] = [p[1], 'B'] # Dummy value on the meantime

    def p_add_op(self, p):
        '''add_op : '''
        # Add previous operator to stack
        self.quadruple_gen.add_operator(p[-1])

    def p_fact_neuro_1(self, p):
        '''fact_neuro_1 :'''
        # Fondo falso
        self.quadruple_gen.add_operator("|")

    def p_fact_neuro_2(self, p):
        '''fact_neuro_2 :'''
        # Fin del fondo falso
        self.quadruple_gen.pop_operator()

    # Variables:
    # - Variable
    # - Elemento de un arreglo de 1 o 2 dimensiones
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

        # Checa si la variable fue declarada con anterioridad
        if not self.func_dir.find_variable(self.last_vars['scope'], p[1][0]):
            print(f'Error: Variable \'{p[1]}\' at line {p.lineno(1)} was not declared.')
            raise Exception(f'Error: Variable \'{p[1]}\' at line {p.lineno(1)} was not declared.')
        p[0] = [0, p[1][1], p[0]]

    # Identificador de la variable
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
            raise Exception(f'Error: Re-declaration of function \'{p[-3]}\'.')

    def p_seen_param(self, p):
        '''seen_param :'''
        # Al llegar a esta regla, significa que hemos visto
        # la declaración de un parámetro.
        # p[-1] es la producción en la que aparece nombre del parámetro
        # p[-2] es la producción en la que aparece el tipo de dato
        if not self.func_dir.add_param(self.last_vars['scope'], p[-1], p[-2]):
            print(f'Error: Re-declaration of function parameter \'{p[-1]}\'.')
            raise Exception(f'Error: Re-declaration of function parameter \'{p[-1]}\'.')

    # Representa Epsilon
    def p_empty(self, p):
        '''empty : '''
        pass

    # Error handling
    def p_error(self, p):
        print("Syntax error in input at line: ", p, p.lineno)
        raise Exception("Syntax error in input at line: ", p, p.lineno)

    # Build parser with initial state
    def build(self, lexer, **kwargs):
        self.func_dir = FunctionsDirectory()
        self.last_vars = {'scope': self.func_dir.GLOBAL_ENV, 'var_type': None}
        self.quadruple_gen = QuadrupleGenerator()

        self.lexer = lexer
        self.parser = yacc.yacc(module=self, **kwargs)

    # Parse input data
    def parse(self, data):
        return self.parser.parse(data)
