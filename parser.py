from lexer import Lexer, tokens, literals

import ply.yacc as yacc

def p_game(p):
    '''game : GAME ID ';' game_vars game_funcs'''
    p[0] = "Aceptado"

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

def p_list_vars(p):
    '''list_vars : ID list_vars_prima'''

def p_list_vars_prima(p):
    '''list_vars_prima : ',' ID list_vars_prima
                       | empty'''

def p_declare_func(p):
    '''declare_func : FUNC ID ':' func_type '(' list_params ')' '{' block_code '}' '''

def p_func_start(p):
    '''func_start : FUNC START ':' VOID '(' ')' '{' block_code '}' '''

def p_func_update(p):
    '''func_update : FUNC UPDATE ':' VOID '(' ')' '{' block_code '}' '''

def p_list_params(p):
    '''list_params : type ID list_params_prima
                   | empty'''

def p_list_params_prima(p):
    '''list_params_prima : ',' type ID list_params_prima
                         | empty'''

def p_func_type(p):
    '''func_type : type
                 | VOID '''

def p_block_code(p):
    '''block_code : block_vars statement_prima
                  | statement statement_prima
                  | empty'''

def p_statement(p):
    '''statement : call_func ';'
                 | for_loop
                 | while_loop
                 | conditional
                 | assignment ';' '''

def p_statement_prima(p):
    '''statement_prima : statement statement_prima
                       | empty'''

def p_call_func(p):
    '''call_func : ID '(' list_args ')' '''

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

def p_type_dims(p):
    '''type_dims : '[' INT_LITERAL ']'
                 | '[' INT_LITERAL ',' INT_LITERAL ']'
                 | empty'''

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
    '''super_exp_prima : REL_OP super_exp
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
            | call_func'''

def p_id_exp(p):
    '''id_exp : ID
              | ID '[' god_exp ']'
              | ID '[' god_exp ',' god_exp ']' '''

def p_empty(p): # representa epsilon
    '''empty : '''
    pass

def p_error(p):
    print("Syntax error in input at line: ", p, p.lineno)

parser = yacc.yacc(debug=True)

# file_name = input("Nombre de archivo: ")
f = open('test.tudi', 'r')
data = f.read()
f.close()

if parser.parse(data) == "Aceptado":
    print("Todo es valido")