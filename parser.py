from lexer import Lexer
import ply.yacc as yacc

def p_game(p):
    ''''''

def p_block_vars(p):
    ''''''

def p_declare_var(p):
    ''''''

def p_list_vars(p):
    '''  '''

def p_statement(p):
    '''  '''

def p_call_func(p):
    '''  '''

def p_list_args(p):
    '''  '''

def p_for_loop(p):
    '''  '''

def p_while_loop(p):
    '''  '''

def p_conditional(p):
    '''  '''

def p_assignment(p):
    '''  '''

def p_declare_func(p):
    '''  '''

def p_list_params(p):
    '''  '''

def p_func_type(p):
    '''  '''

def p_block_code(p):
    '''  '''

def p_func_start(p):
    '''  '''

def p_func_update(p):
    '''  '''

def p_type(p):
    '''  '''

def p_logicop(p):
    '''  '''

def p_relop(p):
    '''  '''

def p_god_exp(p):
    '''  '''

def p_super_exp(p):
    '''  '''

def p_exp(p):
    '''  '''

def p_term(p):
    '''  '''

def p_fact(p):
    '''  '''

def p_id_exp(p):
    ''''''

parser = yacc.yacc()

file_name = input("Nombre de archivo: ")
f = open(file_name, 'r')
data = f.read()
f.close()

if parser.parse(data) == "Aceptado":
    print("Todo es valido")