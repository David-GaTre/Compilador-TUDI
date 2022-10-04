from lexer import Lexer, tokens

import ply.yacc as yacc

def p_game(p):
    '''game : GAME ID SEMICOLON game_vars game_funcs game_start game_update'''
    p[0] = "Aceptado"

def p_game_vars(p):
    '''game_vars : block_vars
                 | empty'''

def p_game_funcs(p):
    '''game_funcs : declare_func game_funcs
                  | empty'''

def p_game_start(p):
    '''game_start : func_start
                  | empty'''

def p_game_update(p):
    '''game_update : func_update 
                   | empty'''

def p_block_vars(p):
    '''block_vars : DECLARE LCURLYB RCURLYB
                  | DECLARE LCURLYB declare_var declare_var_prima RCURLYB'''

def p_declare_var(p):
    '''declare_var : type ID SEMICOLON
                   | type list_vars SEMICOLON'''
    
def p_declare_var_prima(p):
    '''declare_var_prima : declare_var declare_var_prima
                         | empty'''

def p_list_vars(p):
    '''list_vars : LBRACKET ID list_vars_prima RBRACKET '''

def p_list_vars_prima(p):
    '''list_vars_prima : COMMA ID list_vars_prima
                       | empty'''

def p_statement(p):
    '''statement : call_func SEMICOLON
                 | for_loop
                 | while_loop
                 | conditional
                 | assignment SEMICOLON'''

def p_statement_prima(p):
    '''statement_prima : statement statement_prima
                       | empty'''

def p_call_func(p):
    '''call_func : ID LPAREN list_args RPAREN
                 | ID LPAREN RPAREN'''

def p_list_args(p):
    '''list_args : god_exp list_args_prima'''

def p_list_args_prima(p):
    '''list_args_prima : COMMA god_exp list_args_prima
                       | empty'''

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment RPAREN SEMICOLON god_exp SEMICOLON assignment RPAREN LCURLYB block_code RCURLYB'''

def p_while_loop(p):
    '''while_loop : WHILE LPAREN god_exp RPAREN LCURLYB block_code RCURLYB'''

def p_conditional(p):
    '''conditional : IF LPAREN god_exp RPAREN LCURLYB block_code RCURLYB
                   | IF LPAREN god_exp RPAREN LCURLYB block_code RCURLYB ELSE conditional_prima LCURLYB block_code RCURLYB'''

def p_conditional_prima(p):
    '''conditional_prima : conditional
                        | empty'''

def p_assignment(p):
    '''assignment : id_exp ASSIGN god_exp'''

def p_declare_func(p):
    '''declare_func : FUNC ID COLON func_type declare_func_params declare_func_code'''

def p_declare_func_params(p):
    '''declare_func_params : LPAREN RPAREN
                           | LPAREN list_params RPAREN'''

def p_declare_func_code(p):
    '''declare_func_code : LCURLYB RCURLYB
                         | LCURLYB block_code RCURLYB'''

def p_list_params(p):
    '''list_params : type ID list_params_prima'''

def p_list_params_prima(p):
    '''list_params_prima : COMMA type ID list_params_prima
                         | empty'''

def p_func_type(p):
    '''func_type : type
                 | VOID '''

def p_block_code(p):
    '''block_code : block_vars statement statement_prima
                  | statement statement_prima'''

def p_func_start(p):
    '''func_start : FUNC START COLON VOID LPAREN RPAREN LCURLYB RCURLYB
                  | FUNC START COLON VOID LPAREN RPAREN LCURLYB block_code RCURLYB'''

def p_func_update(p):
    '''func_update : FUNC UPDATE COLON VOID LPAREN RPAREN LCURLYB RCURLYB
                   | FUNC UPDATE COLON VOID LPAREN RPAREN LCURLYB block_code RCURLYB'''

def p_type(p):
    '''type : INT type_prima
            | FLOAT type_prima
            | BOOLEAN type_prima
            | CHAR type_prima
            | SPRITE type_prima'''

def p_type_prima(p):
    '''type_prima : LBRACKET INT_LITERAL RBRACKET
                  | LBRACKET INT_LITERAL COMMA INT_LITERAL RBRACKET
                  | empty'''

# Pending to add unary logic operator NOT
def p_logicop(p):
    '''logicop : AND
               | OR'''

def p_relop(p):
    '''relop : GTRTHAN
             | GTREQLTHAN
             | LESSTHAN
             | LESSEQLTHAN
             | EQUALS
             | NOTEQUALS'''

def p_god_exp(p):
    '''god_exp : super_exp god_exp_prima'''

def p_god_exp_prima(p):
    '''god_exp_prima : logicop god_exp
                     | empty'''

def p_super_exp(p):
    '''super_exp : exp super_exp_prima'''

def p_super_exp_prima(p):
    '''super_exp_prima : relop super_exp
                       | empty'''

def p_exp(p):
    '''exp : term exp_prima'''

def p_exp_prima(p):
    '''exp_prima : PLUS term
                  | MINUS term
                  | empty'''

def p_term(p):
    '''term : fact term_prima'''

def p_term_prima(p):
    '''term_prima : DIVISION term
                  | TIMES term
                  | empty'''

def p_fact(p):
    '''fact : LPAREN god_exp RPAREN
            | id_exp
            | INT_LITERAL
            | FLOAT_LITERAL
            | BOOL_LITERAL
            | call_func'''

def p_id_exp(p):
    '''id_exp : ID
              | ID LBRACKET god_exp RBRACKET
              | ID LBRACKET god_exp COMMA god_exp RBRACKET'''

def p_empty(t): # representa epsilon
    '''empty : '''
    pass

def p_error(p):
    print("Syntax error in input at line: ", p, p.lineno)

parser = yacc.yacc(debug=True)

file_name = input("Nombre de archivo: ")
f = open(file_name, 'r')
data = f.read()
f.close()

if parser.parse(data) == "Aceptado":
    print("Todo es valido")