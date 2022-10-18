from lexer import Lexer, tokens, literals, Token
from dir_vars import FunctionsDirectory

import ply.yacc as yacc

func_dir = FunctionsDirectory()
last_vars = {'scope': func_dir.GLOBAL_ENV, 'var_type': None}

def p_game(p):
    '''game : GAME ID ';' CANVAS ASSIGN_OP INT_LITERAL ',' INT_LITERAL ';' game_vars game_funcs'''
    p[0] = "Aceptado"
    print("Todo valido")

    global func_dir
    for func, func_items in func_dir.directory.items():
        print('Scope:', func)
        for func_item, values in func_items.items():
            if func_item == 'table':
                print('\t- Variables:')
                for k, v  in values.table.items():
                    print('\t---', k, v)
            else:
                print('\t-', func_item, ':', values)
        print()

def p_game_vars(p):
    '''game_vars : block_vars
                 | empty'''

def p_game_funcs(p):
    '''game_funcs : declare_func game_funcs 
                  | game_start'''

def p_game_start(p):
    '''game_start : func_start game_update
                  | game_update'''

def p_game_update(p):
    '''game_update : func_update 
                   | empty'''

def p_block_vars(p):
    '''block_vars : DECLARE '{' declare_vars '}' '''

def p_declare_vars(p):
    '''declare_vars : declare_var declare_vars
                    | empty'''

def p_declare_var(p):
    '''declare_var : type list_vars ';' '''
    global last_vars
    last_vars['var_type'] = p[1]
    
    for var_id in p[2]:
        if not func_dir.add_variable(last_vars['scope'], var_id.value, last_vars['var_type']):
            print(f'Error: Re-declaration of variable \'{var_id.value}\' at line: {var_id.lineno}')
            exit()

def p_list_vars(p):
    '''list_vars : ID list_vars_prima'''
    p[0] = [Token(p[1], p.lineno(1))] + p[2]

def p_list_vars_prima(p):
    '''list_vars_prima : ',' ID list_vars_prima
                       | empty'''
    if len(p) > 2:
        p[0] = [Token(p[2], p.lineno(2))] + p[3]
    else:
        p[0] = []

def p_declare_func(p):
    '''declare_func : FUNC ID ':' func_type seen_dec_func '(' list_params ')' '{' block_code '}' '''

def p_func_start(p):
    '''func_start : FUNC START ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

def p_func_update(p):
    '''func_update : FUNC UPDATE ':' VOID seen_dec_func '(' ')' '{' block_code '}' '''

def p_list_params(p):
    '''list_params : type ID seen_param list_params_prima
                   | empty'''

def p_list_params_prima(p):
    '''list_params_prima : ',' type ID seen_param list_params_prima
                         | empty'''

def p_func_type(p):
    '''func_type : type
                 | VOID '''
    p[0] = p[1]

def p_block_code(p):
    '''block_code : block_vars statement_prima
                  | statement statement_prima
                  | empty'''

def p_statement(p):
    '''statement : call_func ';'
                 | for_loop
                 | while_loop
                 | conditional
                 | assignment ';' 
                 | return ';' 
                 | call_method ';' '''

def p_statement_prima(p):
    '''statement_prima : statement statement_prima
                       | empty'''

def p_return(p):
    '''return : RETURN god_exp'''

def p_io_func(p):
    '''io_func : PRINT '(' io_func_prima ')' 
               | READ  '(' io_func_prima ')' '''

def p_io_func_prima(p):
    '''io_func_prima : STRING_LITERAL
                     | empty'''

def p_cast_func(p):
    '''cast_func : INT cast_func_prima 
                 | FLOAT cast_func_prima
                 | BOOLEAN cast_func_prima'''

def p_cast_func_prima(p):
    '''cast_func_prima : '(' STRING_LITERAL ')'
                       | '(' god_exp ')' '''

def p_call_func(p):
    '''call_func : ID '(' list_args ')'
                 | io_func 
                 | cast_func'''

def p_call_method(p):
    '''call_method : id_exp '.' call_method_prima '(' list_args ')' '''

def p_call_method_prima(p):
    '''call_method_prima : SETPOSITION
                         | TRANSLATE
                         | SETCONTROLLABLE '''

def p_list_args(p):
    '''list_args : god_exp list_args_prima
                 | empty'''

def p_list_args_prima(p):
    '''list_args_prima : ',' god_exp list_args_prima
                       | empty'''

def p_for_loop(p):
    '''for_loop : FOR '(' assignment ';' god_exp ';' assignment ')' '{' block_code '}' '''

def p_while_loop(p):
    '''while_loop : WHILE '(' god_exp ')' '{' block_code '}' '''

def p_conditional(p):
    '''conditional : IF '(' god_exp ')' '{' block_code '}' conditional_prima'''

def p_conditional_prima(p):
    '''conditional_prima : ELSE conditional
                         | ELSE '{' block_code '}' 
                         | empty'''

def p_assignment(p):
    '''assignment : id_exp ASSIGN_OP god_exp'''

def p_type(p):
    '''type : INT type_dims
            | FLOAT type_dims
            | BOOLEAN type_dims
            | CHAR type_dims
            | SPRITE type_dims'''
    if p[2] is not None:
        p[0] = "-".join([p[1], p[2]])
    else:
        p[0] = p[1]

def p_type_dims(p):
    '''type_dims : '[' INT_LITERAL ']'
                 | '[' INT_LITERAL ',' INT_LITERAL ']'
                 | empty'''
    if len(p) == 6:
        p[0] = 'arr2d'
    elif len(p) == 4:
        p[0] = 'arr1d'

# Pending to add unary logic operator NOT
def p_logicop(p):
    '''logicop : AND
               | OR'''

def p_god_exp(p):
    '''god_exp : super_exp god_exp_prima'''

def p_god_exp_prima(p):
    '''god_exp_prima : logicop god_exp
                     | empty'''

def p_super_exp(p):
    '''super_exp : exp super_exp_prima'''

def p_super_exp_prima(p):
    '''super_exp_prima : REL_OP exp
                       | empty'''

def p_exp(p):
    '''exp : term exp_prima'''

def p_exp_prima(p):
    '''exp_prima : '+' exp
                 | '-' exp
                 | empty'''

def p_term(p):
    '''term : fact term_prima'''

def p_term_prima(p):
    '''term_prima : '/' term
                  | '*' term
                  | empty'''

def p_fact(p):
    '''fact : '(' god_exp ')'
            | id_exp
            | INT_LITERAL
            | FLOAT_LITERAL
            | BOOL_LITERAL
            | call_func '''

def p_id_exp(p):
    '''id_exp : ID
              | ID '[' god_exp ']'
              | ID '[' god_exp ',' god_exp ']' '''

def p_seen_dec_func(p):
    '''seen_dec_func :'''
    # Al llegar a esta regla, significa que hemos visto el inicio de
    # la declaración de una función.
    # p[-1] es la producción en la que aparece el tipo de retorno
    # p[-3] es la producción en la que aparece el nombre de la función
    global last_vars
    last_vars['scope'] = p[-3]
    if not func_dir.add_function(last_vars['scope'], p[-1]):
        print(f'Error: Re-declaration of function \'{p[-3]}\'.')
        exit()

def p_seen_param(p):
    '''seen_param :'''
    # Al llegar a esta regla, significa que hemos visto
    # la declaración de un parámetro.
    # p[-1] es la producción en la que aparece nombre del parámetro
    # p[-2] es la producción en la que aparece el tipo de dato
    if not func_dir.add_param(last_vars['scope'], p[-1], p[-2]):
        print(f'Error: Re-declaration of function parameter \'{p[-1]}\'.')
        exit()

def p_empty(p): # representa epsilon
    '''empty : '''
    pass

def p_error(p):
    print("Syntax error in input at line: ", p, p.lineno)
    exit()

parser = yacc.yacc(debug=True)

# file_name = input("Nombre de archivo: ")
f = open('test.tudi', 'r')
data = f.read()
f.close()

parser.parse(data)