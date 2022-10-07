import ply.lex as lex

reserved = {
    'Start' : 'START',
    'Update': 'UPDATE',
    'game': 'GAME',
    'int': 'INT',
    'float' : 'FLOAT',
    'bool': 'BOOLEAN',
    'char': 'CHAR',
    'void': 'VOID',
    'canvas': 'CANVAS',
    'sprite': 'SPRITE',
    'func': 'FUNC',
    'return': 'RETURN',
    'declare': 'DECLARE',
    'print': 'PRINT',
    'read': 'READ',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'y': 'AND',
    'o': 'OR',
    'no': 'NOT'
}

tokens = [
    'REL_OP',
    'ASSIGN_OP',
    'ID',
    'INT_LITERAL', 'FLOAT_LITERAL', 'BOOL_LITERAL', 'STRING_LITERAL']
    
tokens = tokens + list(reserved.values())

# Character literal tokens:
# - COMMA, COLON, SEMICOLON, DOT
# - LEFT_PAREN, RIGHT_PAREN,
# - LEFT_BRACKET, RIGHT_BRACKET,
# - LEFT_CURLY, RIGHT_CURLY,
# - PLUS, MINUS, TIMES, DIVIDE
literals = [',', ':', ';', '.', 
            '(', ')',
            '[', ']',
            '{', '}',
            '+', '-', '*', '/']

t_ASSIGN_OP = r'='
t_REL_OP = r'<|<=|==|>|>=|!='

# Ignore these chars (spaces and tabs)
t_ignore  = ' \t'

def t_BOOL_LITERAL(t):
     r'(true)|(false)'
     t.value = bool(t.value == 'true')
     return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t

def t_STRING_LITERAL(t):
    r'\"(\w|\s)+\"' # for word and space chars
    return t

def t_FLOAT_LITERAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

Lexer = lex.lex()