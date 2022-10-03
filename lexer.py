import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'start' : 'START',
    'update': 'UPDATE',
    'game': 'GAME',
    'int': 'INT',
    'float' : 'FLOAT',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'void': 'VOID',
    'canvas': 'CANVAS',
    'sprite': 'SPRITE',
    'func': 'FUNC',
    'return': 'RETURN',
    'declare': 'DECLARE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE'
}

tokens = ['SEMICOLON', 'COLON', 'COMMA', 'ASSIGN', 'LCURLYB', 'RCURLYB', 'LPAREN',
    'RPAREN', 'LBRACKET', 'RBRACKET', 'PLUS', 'MINUS', 'DIVISION', 'TIMES','GTRTHAN', 
    'GTREQLTHAN', 'LESSTHAN', 'LESSEQLTHAN', 'EQUALS', 'NOTEQUALS','AND', 'OR', 'NOT',
    'INT_LITERAL', 'FLOAT_LITERAL', 'BOOL_LITERAL', 'STRING_LITERAL', 'ID'] + list(reserved.values())

t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_ASSIGN = r'\='
t_LCURLYB = r'\{'
t_RCURLYB = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVISION = r'\/'
t_TIMES = r'\*'
t_GTRTHAN = r'\>'
t_GTREQLTHAN = r'\>\='
t_LESSTHAN = r'\<'
t_LESSEQLTHAN = r'\<\='
t_EQUALS = r'\=\='
t_NOTEQUALS = r'\!\='
t_AND = r'\y'
t_OR = r'\o'
t_NOT = r'\n\o'
t_INT_LITERAL = r'[0-9]+'
t_FLOAT_LITERAL = r'[0-9]+(\. [0-9]+)'
t_BOOL_LITERAL = r'(true) | (false)'
t_STRING_LITERAL = r'\"(\w+|\s)+\"' # for word and space chars
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