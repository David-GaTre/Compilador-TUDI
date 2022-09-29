import ply.lex as lex
import ply.yacc as yacc

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'game' : 'GAME',
   'start' : 'START',
   'float' : 'FLOAT',
   'int' : 'INT',
   'for': 'FOR',
   'while': 'WHILE'
}

tokens = ['SEMICOLON','COLON', 'COMMA', 'EQUALS', 'LCURLYB', 'RCURLYB', 
    'LPAREN','RPAREN', 'PLUS', 'MINUS', 'DIVISION', 'TIMES',
    'CTE_I', 'CTE_F', 'CTE_STRING', 'ID', 'RELOP'] + list(reserved.values())

t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_EQUALS = r'\='
t_LCURLYB = r'\{'
t_RCURLYB = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVISION = r'\/'
t_TIMES = r'\*'
t_CTE_I = r'[0-9]+'
t_CTE_F = r'[0-9]+(\. [0-9]+)'
t_CTE_STRING = r'\"(\w+|\s)+\"' # for word and space chars
t_ignore  = ' \t'

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()