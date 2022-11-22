from lexer import LexerTudi, Token
from dir_vars import FunctionsDirectory
from sem_cube import SemanticCube
from quadruples import QuadrupleGenerator, type_to_char, char_to_type
from memory import VirtualMemory

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
        '''game : GAME ID ';' CANVAS ASSIGN_OP int ',' int ';' game_vars game_funcs'''
        self.quadruple_gen.quadruples[0].temp = self.quadruple_gen.count_q
        self.quadruple_gen.add_quad_from_parser("ERA", None, None, 'Start')
        self.quadruple_gen.add_quad_from_parser("GOSUB", None, None, 'Start')
        self.quadruple_gen.add_quad_from_parser("ERA", None, None, 'Update')
        self.quadruple_gen.add_quad_from_parser("GOSUB", None, None, 'Update')
        p[0] = "Aceptado"
        if self.verbose:
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

            print("Constant table:")
            print(self.virtual_mem.constant_table)
            print()

            self.quadruple_gen.print_quadruples()

    # Declaración de variables globales (opcional)
    def p_game_vars(self, p):
        '''game_vars : block_vars
                     | empty'''
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, None)

    # Definición de funciones:
    # - Funciones definidas por el usuario (opcionales)
    # - Llenar funciones Start y Update de TUDI (obligatorias)
    #   con código del usuario
    def p_game_funcs(self, p):
        '''game_funcs : declare_func game_funcs
                      | func_start func_update'''

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
        self.last_vars['var_type'] = p[1][0]

        # Checar por nombres de variables duplicadas en el scope actual
        for var_id in p[2]:
            increment = p[1][1][0]
            dims = p[1][1][1]

            if self.last_vars['scope'] == '0':
                mem_address = self.virtual_mem.get_new_global(type_to_char[self.last_vars['var_type']], increment)
            else:
                mem_address = self.virtual_mem.get_new_local(type_to_char[self.last_vars['var_type']], increment)

            # Se guarda la dirección de memoria si es un arreglo,
            # pueste que es la constante que se usará para la dirección base
            if dims is not None:
                self.virtual_mem.get_constant_address(mem_address, 'I')

            if not self.func_dir.add_variable(self.last_vars['scope'], var_id.value, self.last_vars['var_type'], mem_address, dims, increment):
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
        '''declare_func : FUNC ID ':' func_type seen_dec_func '(' list_params ')' '{' block_vars_code '}' '''
        # Si hay valor de retorno, entonces el ENDFUNC tiene en la última casilla
        # el tipo de retorno. Este es usado para detectar en ejecución, que si se llega
        # a un quad así esta función no regreso nada y marcar error.
        return_type = None
        if isinstance(p[4], list) and p[4][0] != 'void':
            return_type = p[4][0]
        self.quadruple_gen.add_quad_from_parser("ENDFUNC", None, None, return_type)
        self.func_dir.add_resources(p[2], self.virtual_mem.get_temps_and_locals())
        self.func_dir.clear_var_table(p[2])
        self.virtual_mem.reset_temps_and_locals()

    # Definición de función Start de TUDI:
    # - Si está presente en el programa, la función Start es
    #   la primera en ejecutarse
    def p_func_start(self, p):
        '''func_start : FUNC START ':' VOID seen_dec_func '(' ')' '{' block_vars_code '}' '''
        self.quadruple_gen.add_quad_from_parser("ENDFUNC", None, None, None)
        self.func_dir.add_resources(p[2], self.virtual_mem.get_temps_and_locals())
        self.func_dir.clear_var_table(p[2])
        self.virtual_mem.reset_temps_and_locals()

    # Definición de función Update de TUDI:
    # - Si está presente en el programa, la función Update es
    #   la función que está siendo ejecutada constantemente (loop)
    def p_func_update(self, p):
        '''func_update : FUNC UPDATE ':' VOID seen_dec_func '(' ')' '{' block_vars_code '}' '''
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, self.func_dir.find_function('Update')["start"])
        self.quadruple_gen.add_quad_from_parser("ENDFUNC", None, None, None)
        self.func_dir.add_resources(p[2], self.virtual_mem.get_temps_and_locals())
        self.func_dir.clear_var_table(p[2])
        self.virtual_mem.reset_temps_and_locals()

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
        if len(p[1]) == 2:
            p[0] = p[1]
            if p[1][1][1] is not None:
                raise Exception(f"Functions return values cannot be arrays")
        else:
            p[0] = [p[1], 0]

    # Bloque de código con posibles variables, puede incluir:
    # - Bloque de declaración de variables
    # - Estatutos
    def p_block_vars_code(self, p):
        '''block_vars_code : block_vars statement_prima
                           | statement statement_prima
                           | empty'''

    # Bloque de código solamente, puede incluir:
    # - Estatutos
    def p_block_code(self, p):
        '''block_code : statement statement_prima
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
                     | return ';' '''

    # Añadir un estatuto más
    def p_statement_prima(self, p):
        '''statement_prima : statement statement_prima
                           | empty'''

    # Estatuto de retorno:
    # - Regresa una expresión
    def p_return(self, p):
        '''return : RETURN god_exp '''
        # Checar que se está en una función que regresa un valor y que este sea del mismo tipo
        if not self.func_dir.find_function(self.last_vars['scope']):
            raise Exception(f"Something went wrong... at line: {p.lineno(1)}")

        func = self.func_dir.find_function(self.last_vars['scope'])
        t_type, operand = self.quadruple_gen.pop_operand()
        if type_to_char[func["return_type"]] != t_type:
            raise Exception(f"Return expected a value of type {func['return_type']}, but got {char_to_type[t_type]} at line: {p.lineno(1)}")

        self.quadruple_gen.add_quad_from_parser("RET", None, None, operand)

    # Funciones built-in de I/O en TUDI:
    # - Print: Muestra en consola el argumento provisto
    # - Read: Pide input del usuario, como prompt utiliza
    #         el argumento provisto. Retorna un string literal
    def p_io_func(self, p):
        '''io_func : print
                   | read '''
        p[0] = [p[1], "V"]

    def p_print(self, p):
        '''print : PRINT '(' STRING_LITERAL ')'
                 | PRINT '(' god_exp ')' '''
        p[0] = p[1]
        # Pop resultado de expresión
        if p[3] is None:
            _, output = self.quadruple_gen.pop_operand()
        else:
            output = p[3]

        self.quadruple_gen.add_quad_from_parser(p[1], None, None, output)

    def p_read(self, p):
        '''read : READ '(' id_exp ')' '''
        p[0] = p[1]
        self.quadruple_gen.add_quad_from_parser(p[1], None, None, p[3][0])

    # Funciones built-in de cast en TUDI:
    # - Para los tipos de datos: int, float y bool
    # - Reciben un string literal o un arreglo de chars
    def p_cast_func(self, p):
        '''cast_func : INT cast_func_prima
                     | FLOAT cast_func_prima
                     | BOOLEAN cast_func_prima'''
        func = {'name': p[1]} | self.func_dir.find_function(p[1])

        self.quadruple_gen.add_quad_from_parser("CAST", p[1], func["return_address"], p[2])
        t_type = type_to_char[p[1]]

        t = self.virtual_mem.get_new_temporal(t_type)
        self.quadruple_gen.add_assignment(t, func["return_address"])

        p[0] = [t, t_type]

    # El argumento posible de una función de cast:
    # - String literal o arreglo de chars
    def p_cast_func_prima(self, p):
        '''cast_func_prima : '(' STRING_LITERAL ')'
                           | '(' god_exp ')' '''
        if p[2] is None:
            _, output = self.quadruple_gen.pop_operand()
        else:
            output = p[2]
        p[0] = output

    # Llamada a una función
    def p_call_func(self, p):
        '''call_func : ID call_neuro_1 '(' call_neuro_2 seen_fact_open list_args_func ')' seen_fact_close
                     | io_func
                     | cast_func'''
        if len(p) > 2:
            # Verifica que se pasaron la cantidad necesaria de parámetros
            func, param_counter = self.quadruple_gen.params_stack.pop()
            if param_counter != len(func["params"]):
                print(f"Error: Function {func['name']} expected {len(func['params'])} arguments, but got {param_counter}.")
                raise Exception(f"Error: Function {func['name']} expected {len(func['params'])} arguments, but got {param_counter}.")
            # Genera GOSUB
            self.quadruple_gen.add_quad_from_parser("GOSUB", None, None, func["name"])
            # Guarda valor si no es void
            if func['return_type'] != "void":
                t = self.virtual_mem.get_new_temporal(type_to_char[func['return_type']])
                self.quadruple_gen.add_assignment(t, func["return_address"])
                p[0] = [t, type_to_char[func['return_type']], p[0]]
            else:
                p[0] = [func["name"], type_to_char[func['return_type']], p[0]] # Dummy value in the meantime
        else:
            p[0] = p[1]

    def p_call_neuro_1(self, p):
        '''call_neuro_1 : '''
        # Checa que exista una función definida por el usuario
        # p[-1] es la producción en la que aparece el nombre de la función
        if not self.func_dir.find_function(p[-1]):
            print(f'Error: Function \'{p[-1]}\' at line {p.lineno(-1)} was not declared.')
            raise Exception(f'Error: Function \'{p[-1]}\' at line {p.lineno(-1)} was not declared.')
        func = {'name': p[-1]} | self.func_dir.find_function(p[-1])
        p[0] = func

    def p_call_neuro_2(self, p):
        '''call_neuro_2 : '''
        # Genera ERA
        # p[-2] es la producción en la que aparecen los atributos de la función
        self.quadruple_gen.add_quad_from_parser("ERA", None, None, p[-2]["name"])
        self.quadruple_gen.params_stack.append([p[-2], 0])

    def p_call_neuro_3(self, p):
        '''call_neuro_3 : '''
        # Pop
        t_type, operand = self.quadruple_gen.pop_operand()
        # Verifica el parametro
        func, param_counter = self.quadruple_gen.params_stack[-1]
        if param_counter >= len(func["params"]):
            print(f"Error: Function {func['name']} expected {len(func['params'])} arguments, but got more than needed.")
            raise Exception(f"Error: Function {func['name']} expected {len(func['params'])} arguments, but got more than needed.")

        if t_type != type_to_char[func["params"][param_counter][0]]:
            print(f"Error: Function {func['name']} expected argument {param_counter + 1} of type {func['params'][param_counter][0]}, but got {char_to_type[t_type]}.")
            raise Exception(f"Error: Function {func['name']} expected argument {param_counter + 1} of type {func['params'][param_counter][0]}, but got {char_to_type[t_type]}.")

        # Genera PARAM
        self.quadruple_gen.add_quad_from_parser("PARAM", operand, None, f"par{param_counter + 1}")
        self.quadruple_gen.params_stack[-1][1] += 1

    # Lista de argumentos (expresiones)
    def p_list_args_func(self, p):
        '''list_args_func : god_exp call_neuro_3 list_args_func_prima
                     | empty'''

    # Añadir un argumento a la lista de argumentos
    def p_list_args_func_prima(self, p):
        '''list_args_func_prima : ',' god_exp call_neuro_3 list_args_func_prima
                           | empty'''

    # Ciclo for loop (C/C++ style)
    def p_for_loop(self, p):
        '''for_loop : FOR '(' assignment ';' for_neuro_1 god_exp for_neuro_2 ';' for_neuro_3 assignment for_neuro_4 ')' '{' cond_neuro_2 block_code '}' cond_neuro_3 for_neuro_5 '''
    
    def p_for_neuro_1(self, p):
        '''for_neuro_1 : '''
        # Marcar inicio de evaluación de expresión condicional
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)

    def p_for_neuro_2(self, p):
        '''for_neuro_2 : '''
        c_type, operand  = self.quadruple_gen.pop_operand()
        # Checar que la expresión sea de tipo: Bool, Int o Float
        if c_type not in ['B', 'I', 'F']:
           raise Exception(f"Type mismatch: Expecting a boolean, int or float, instead got {char_to_type[c_type]}.")
        # Agregar GOTO_F
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO_F", operand, None, None)
        # Agregar GOTO_V
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO_V", operand, None, None)

    def p_for_neuro_3(self, p):
        '''for_neuro_3 : '''
        # Marcar inicio de evaluación de expresión de actualización
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)

    def p_for_neuro_4(self, p):
        '''for_neuro_4 : '''
        # Agregar GOTO
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, None)

    def p_for_neuro_5(self, p):
        '''for_neuro_5 : '''
        # Recuperar todos los valores relacionados al for
        goto_cond = self.quadruple_gen.goto_stack.pop()
        prev_eval_update = self.quadruple_gen.goto_stack.pop()
        goto_V = self.quadruple_gen.goto_stack.pop()
        goto_F = self.quadruple_gen.goto_stack.pop()
        prev_eval_cond = self.quadruple_gen.goto_stack.pop()
        # Agregar GOTO a update
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, prev_eval_update)
        # Llenar GOTO cond a inicio condición
        self.quadruple_gen.quadruples[goto_cond - 1].temp = prev_eval_cond
        # Llenar GOTO V a después de GOTO cond
        self.quadruple_gen.quadruples[goto_V - 1].temp = goto_cond + 1
        # Llenar GOTO F a después de GOTO update (a.k.a current count_q)
        self.quadruple_gen.quadruples[goto_F - 1].temp = self.quadruple_gen.count_q

    # Ciclo while clásico (C/C++ style)
    def p_while_loop(self, p):
        '''while_loop : WHILE while_neuro_1 '(' god_exp while_neuro_2 ')' '{' cond_neuro_2 block_code '}' cond_neuro_3 while_neuro_3 '''

    def p_while_neuro_1(self, p):
        '''while_neuro_1 : '''
        # Marcar inicio de evaluación de expresión condicional
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)

    def p_while_neuro_2(self, p):
        '''while_neuro_2 : '''
        c_type, operand  = self.quadruple_gen.pop_operand()
        # Checar que la expresión sea de tipo: Bool, Int o Float
        if c_type not in ['B', 'I', 'F']:
           raise Exception(f"Type mismatch: Expecting a boolean, int or float, instead got {char_to_type[c_type]}.")
        # Agregar GOTO_F
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO_F", operand, None, None)

    def p_while_neuro_3(self, p):
        '''while_neuro_3 : '''
        # Recuperar GOTO_F e inicio de evaluación de expresión de condición
        goto_f = self.quadruple_gen.goto_stack.pop()
        prev_eval_cond = self.quadruple_gen.goto_stack.pop()
        # Agregar GOTO para regresar a evaluación
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, prev_eval_cond)
        # Llenar GOTO_F pasado
        self.quadruple_gen.quadruples[goto_f - 1].temp = self.quadruple_gen.count_q

    # If condicional (C/C++ style)
    def p_conditional(self, p):
        '''conditional : IF '(' god_exp ')' cond_neuro_1 '{' cond_neuro_2 block_code '}' cond_neuro_3 conditional_prima '''
        
    # Else-If / Else condicional (C/C++ style)
    def p_conditional_prima(self, p):
        '''conditional_prima : ELSE cond_neuro_4 conditional 
                             | ELSE cond_neuro_4 '{' cond_neuro_2 block_code '}' cond_neuro_3 cond_neuro_5
                             | empty cond_neuro_5'''

    def p_cond_neuro_1(self, p):
        '''cond_neuro_1 : '''
        # Agregar GOTO_F
        god_exp_type, operand  = self.quadruple_gen.pop_operand()
        # Checar que la expresión sea de tipo: Bool, Int o Float
        if god_exp_type not in ['B', 'I', 'F']:
           raise Exception(f"Type mismatch: Expecting a boolean, int or float, instead got {char_to_type[god_exp_type]}.")
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO_F", operand, None, self.quadruple_gen.count_q)

    def p_cond_neuro_2(self, p):
        '''cond_neuro_2 : '''
        # Agregar fondo falso
        self.quadruple_gen.goto_stack.append("|")

    def p_cond_neuro_3(self, p):
        '''cond_neuro_3 : '''
        # Quitar fondo falso
        self.quadruple_gen.goto_stack.pop()

    def p_cond_neuro_4(self, p):
        '''cond_neuro_4 : '''
        # Recuperar GOTO_F pasado
        prev_goto_f = self.quadruple_gen.goto_stack.pop()
        # Agregar GOTO
        self.quadruple_gen.goto_stack.append(self.quadruple_gen.count_q)
        self.quadruple_gen.add_quad_from_parser("GOTO", None, None, self.quadruple_gen.count_q)
        # Llenar GOTO_F pasado
        self.quadruple_gen.quadruples[prev_goto_f - 1].temp = self.quadruple_gen.count_q

    def p_cond_neuro_5(self, p):
        '''cond_neuro_5 : '''
        # Recuperar y llenar GOTOs
        while len(self.quadruple_gen.goto_stack) > 0 and self.quadruple_gen.goto_stack[-1] != "|":
            prev_goto = self.quadruple_gen.goto_stack.pop()
            self.quadruple_gen.quadruples[prev_goto - 1].temp = self.quadruple_gen.count_q

    # Asignación de una expresión a una variables:
    # - Se debe verificar que los tipos de datos coincidan
    def p_assignment(self, p):
        '''assignment : id_exp ASSIGN_OP god_exp '''
        t_type, operand = self.quadruple_gen.pop_operand()
        # Checar que id_exp sea del mismo tipo que la expresión
        # id_exp: [name, type]
        if p[1][1] != t_type:
            print(f'Error: Cannot assign value of type \'{char_to_type[t_type]}\' to variable \'{p[1][0]}\' of type \'{char_to_type[p[1][1]]}\' at line {p.lineno(2)}.')
            raise Exception(f'Error: Cannot assign value of type \'{char_to_type[t_type]}\' to variable \'{p[1][0]}\' of type \'{char_to_type[p[1][1]]}\' at line {p.lineno(2)}.')
        self.quadruple_gen.add_assignment(p[1][0], operand)

    # Tipos de datos en TUDI:
    # - Pueden ser arreglos de 1 o 2 dimensiones
    def p_type(self, p):
        '''type : INT type_dims
                | FLOAT type_dims
                | BOOLEAN type_dims
                | CHAR type_dims'''
        # TODO: Implementar arreglos correctamente
        # if p[2] is not None:
        #     p[0] = "-".join([p[1], p[2]])
        # else:
        #     p[0] = p[1]
        p[0] = [p[1], p[2]]

    # En la declaración, los arreglos solamente
    # aceptan int literals para la definición del tamaño
    def p_type_dims(self, p):
        '''type_dims : '[' int ']'
                     | '[' int ',' int ']'
                     | empty'''
        if len(p) == 6:
            if p[2][2] <= 0 or p[4][2] <= 0:
                raise Exception(f"Array dimensions must be greater than 0")
            m0 = p[2][2] * p[4][2]
            bound1 = self.virtual_mem.get_constant_address(p[2][2], 'I')
            bound2 = self.virtual_mem.get_constant_address(p[4][2], 'I')
            m1 = self.virtual_mem.get_constant_address(p[4][2], 'I')
            zero = self.virtual_mem.get_constant_address(0, 'I')

            # Limite superior 1 y m1
            dim1 = (bound1, m1)
            # Limite superior 2 y (-K)
            dim2 = (bound2, zero)

            p[0] = (m0, [dim1, dim2])
        elif len(p) == 4:
            if p[2][2] <= 0:
                raise Exception(f"Array dimensions must be greater than 0")
            bound1 = self.virtual_mem.get_constant_address(p[2][2], 'I')
            zero = self.virtual_mem.get_constant_address(0, 'I')

            # Limite superior 1 y (-K)
            dim1 = (bound1, zero)
            p[0] = (p[2][2], [dim1])
        else:
            p[0] = (1, None)

    # Expresión (lógica, relacional, aritmética)
    def p_god_exp(self, p):
        '''god_exp : super_exp seen_super_exp god_exp_prima'''
        self.quadruple_gen.finish_expression(sem_cube, self.virtual_mem)

    def p_seen_super_exp(self, p):
        '''seen_super_exp : '''
        self.quadruple_gen.check_stack_operand(arr_logicops, sem_cube, self.virtual_mem)

    # Operadores lógicos
    def p_god_exp_prima(self, p):
        '''god_exp_prima : LOGIC_OPS seen_op god_exp
                         | empty'''

    def p_super_exp(self, p):
        '''super_exp : exp super_exp_prima seen_exp'''

    def p_seen_exp(self, p):
        '''seen_exp : '''
        self.quadruple_gen.check_stack_operand(arr_relops, sem_cube, self.virtual_mem)

    # Operadores relacionales
    def p_super_exp_prima(self, p):
        '''super_exp_prima : REL_OPS seen_op exp
                           | empty'''

    def p_exp(self, p):
        '''exp : term seen_term exp_prima'''

    def p_seen_term(self, p):
        '''seen_term : '''
        self.quadruple_gen.check_stack_operand(["+", "-"], sem_cube, self.virtual_mem)

    # Operadores suma y resta
    def p_exp_prima(self, p):
        '''exp_prima : '+' seen_op exp
                     | '-' seen_op exp
                     | empty'''

    def p_term(self, p):
        '''term : fact seen_fact term_prima'''

    def p_seen_fact(self, p):
        '''seen_fact : '''
        self.quadruple_gen.check_stack_operand(["*", "/"], sem_cube, self.virtual_mem)

    # Operadores de multiplación y división
    def p_term_prima(self, p):
        '''term_prima : '/' seen_op term
                      | '*' seen_op term
                      | empty'''

    # Factores de una expresión:
    # - Operadores de agrupacion (paréntesis)
    # - Variables y literals
    # - Llamadas a una función (lo que retorna)
    def p_fact(self, p):
        '''fact : '(' seen_fact_open god_exp ')' seen_fact_close
                | fact_constants
                | '-' seen_unary fact
                | NOT seen_unary fact '''

        if len(p) == 2:
            # (Type, operand)
            self.quadruple_gen.add_operand(p[1][1], p[1][0])
        if p[1] == '-' or p[1] == 'no':
            self.quadruple_gen.check_stack_operand(["-", "no"], sem_cube, self.virtual_mem)
        p[0] = p[1]

    def p_seen_unary(self, p):
        '''seen_unary : '''
        self.quadruple_gen.add_operator(p[-1])
        self.quadruple_gen.add_operand("U", self.virtual_mem.get_constant_address(0, 'I'))

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
        address = self.virtual_mem.get_constant_address(p[1], 'I')
        p[0] = [address, 'I', p[1]]

    # Flotantes
    def p_float(self, p):
        '''float : FLOAT_LITERAL'''
        address = self.virtual_mem.get_constant_address(p[1], 'F')
        p[0] = [address, 'F', p[1]]

    # Booleanos
    def p_bool(self, p):
        '''bool : BOOL_LITERAL'''
        address = self.virtual_mem.get_constant_address(p[1], 'B')
        p[0] = [address, 'B', p[1]]

    def p_seen_op(self, p):
        '''seen_op : '''
        # Add previous operator to stack
        self.quadruple_gen.add_operator(p[-1])

    def p_seen_fact_open(self, p):
        '''seen_fact_open :'''
        # Fondo falso
        self.quadruple_gen.add_operator("|")

    def p_seen_fact_close(self, p):
        '''seen_fact_close :'''
        # Fin del fondo falso
        self.quadruple_gen.pop_operator()

    # Variables:
    # - Variable
    # - Elemento de un arreglo de 1 o 2 dimensiones
    def p_id_exp(self, p):
        '''id_exp : ID check_id
                  | ID check_id '[' seen_fact_open god_exp ']' seen_dim1 seen_fact_close
                  | ID check_id '[' seen_fact_open god_exp seen_fact_close seen_dim2_1 ',' seen_fact_open god_exp ']' seen_fact_close  seen_dim2_2 '''
        if len(p) > 3:
            t_type, operand = self.quadruple_gen.pop_operand()
            p[0] = [operand, t_type]
        else:
            var= p[2]
            p[0] = [var['address'], type_to_char[var["type"]]]

    def p_check_id(self, p):
        '''check_id : '''
        # Checa si la variable fue declarada con anterioridad
        if not self.func_dir.find_variable(self.last_vars['scope'], p[-1]):
            print(f'Error: Variable \'{p[-1]}\' at line {p.lineno(-1)} was not declared.')
            raise Exception(f'Error: Variable \'{p[-1]}\' at line {p.lineno(-1)} was not declared.')

        p[0] = {"name": p[-1]} | self.func_dir.find_variable(self.last_vars['scope'], p[-1])

    def p_seen_dim1(self, p):
        '''seen_dim1 : '''
        # Checar si la variable es un arreglo de una dimensión
        var = p[-5]
        if len(var["dims"]) != 1:
            raise Exception(f'Error: Variable \'{var["name"]}\' is not an array')

        # Checar que el operando es de tipo entero
        t_type, operand = self.quadruple_gen.pop_operand()
        if t_type != 'I':
            raise Exception(f'Error: Index of {var["name"]} must be an integer')

        # Agrega quad VER para verificar en ejecución que
        # el operando esté dentro de los límites [0, var[dims][0][0])
        self.quadruple_gen.add_quad_from_parser('VER', operand, None, var["dims"][0][0])

        # Suma el operando a la dirección base y lo guarda en un temporal pointer
        temp_pointer = self.virtual_mem.get_new_temporal('P')
        dirBase = self.virtual_mem.get_constant_address(var["address"], 'I')
        self.quadruple_gen.add_operand(type_to_char[var["type"]], temp_pointer)
        self.quadruple_gen.add_quad_from_parser('+', operand, dirBase, temp_pointer)

    
    def p_seen_dim2_1(self, p):
        '''seen_dim2_1 : '''
        # Checar si la variable es un arreglo de dos dimensiones
        var = p[-5]
        if len(var["dims"]) != 2:
            raise Exception(f'Error: Variable \'{var["name"]}\' is not a matrix')

        # Checar que el operando es de tipo entero
        t_type, operand = self.quadruple_gen.pop_operand()
        if t_type != 'I':
            raise Exception(f'Error: Index of {var["name"]} must be an integer')

        # Agrega quad VER para verificar en ejecución que
        # el operando esté dentro de los límites [0, var[dims][0][0])
        self.quadruple_gen.add_quad_from_parser('VER', operand, None, var["dims"][0][0])

        # Multiplica el operando * m1
        temp_int = self.virtual_mem.get_new_temporal('I')
        self.quadruple_gen.add_quad_from_parser('*', operand, var["dims"][0][1], temp_int)
        self.quadruple_gen.add_operand('I', temp_int)

    def p_seen_dim2_2(self, p):
        '''seen_dim2_2 : '''
        # Checar si la variable es un arreglo de dos dimensiones
        var = p[-11]

        # Checar que el operando es de tipo entero
        t_type, operand = self.quadruple_gen.pop_operand()
        if t_type != 'I':
            raise Exception(f'Error: Index of {var["name"]} must be an integer')

        # Agrega quad VER para verificar en ejecución que
        # el operando esté dentro de los límites [0, var[dims][1][0])
        self.quadruple_gen.add_quad_from_parser('VER', operand, None, var["dims"][1][0])

        # Suma el operando y k
        t_type_sm, operand_sm = self.quadruple_gen.pop_operand()
        if t_type_sm != 'I':
            raise Exception(f'Error: Index of {var["name"]} must be an integer')

        temp_int = self.virtual_mem.get_new_temporal('I')
        self.quadruple_gen.add_quad_from_parser('+', operand_sm, operand, temp_int)

        # Suma el operando a la dirección base y lo guarda en un temporal pointer
        temp_pointer = self.virtual_mem.get_new_temporal('P')
        dirBase = self.virtual_mem.get_constant_address(var["address"], 'I')
        self.quadruple_gen.add_operand(type_to_char[var["type"]], temp_pointer)
        self.quadruple_gen.add_quad_from_parser('+', temp_int, dirBase, temp_pointer)

    def p_seen_dec_func(self, p):
        '''seen_dec_func :'''
        # Al llegar a esta regla, significa que hemos visto el inicio de
        # la declaración de una función.
        # p[-1] es la producción en la que aparece el tipo de retorno
        # p[-3] es la producción en la que aparece el nombre de la función
        self.last_vars['scope'] = p[-3]

        if isinstance(p[-1], list):
            return_type = p[-1][0]
        else:
            return_type = p[-1]
        if not self.func_dir.add_function(self.last_vars['scope'], return_type, self.quadruple_gen.count_q):
            print(f'Error: Re-declaration of function \'{p[-3]}\'.')
            raise Exception(f'Error: Re-declaration of function \'{p[-3]}\'.')

        # Agrega como variable global el nombre de la función como lo visto en clase
        if return_type != "void":
            mem_address = self.virtual_mem.get_new_global(type_to_char[return_type], p[-1][1][0])
            self.func_dir.add_return_address(self.last_vars['scope'], mem_address)

    def p_seen_param(self, p):
        '''seen_param :'''
        # Al llegar a esta regla, significa que hemos visto
        # la declaración de un parámetro.
        # p[-1] es la producción en la que aparece nombre del parámetro
        # p[-2] es la producción en la que aparece el tipo de dato
        dims = p[-2][1][1]
        if dims is not None:
            raise Exception(f"Functions parameters cannot be arrays")

        mem_address = self.virtual_mem.get_new_local(type_to_char[p[-2][0]])

        if not self.func_dir.add_param(self.last_vars['scope'], p[-1], p[-2][0], mem_address, dims):
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
    def build(self, lexer, verbose=False, **kwargs):
        self.func_dir = FunctionsDirectory()
        self.last_vars = {'scope': self.func_dir.GLOBAL_ENV, 'var_type': None}
        self.quadruple_gen = QuadrupleGenerator()
        self.virtual_mem = VirtualMemory()
        self.verbose = verbose

        # Built-in function with parametric polymorphism
        for func in ["int", "float", "bool"]:
            self.func_dir.add_function(func, func, None)
            mem_address = self.virtual_mem.get_new_global(type_to_char[func])
            self.func_dir.add_return_address(func, mem_address)

        self.lexer = lexer
        self.parser = yacc.yacc(module=self, **kwargs)

    # Parse input data
    def parse(self, data):
        return self.parser.parse(data)

    def get_quadruples(self):
        return self.quadruple_gen.quadruples

    def get_function_directory(self):
        return self.func_dir

    def get_constant_table(self):
        return {v.address: v.value for k, v in self.virtual_mem.constant_table.items()}