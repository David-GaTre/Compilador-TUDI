import ply.lex as lex

class Token:
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

# Palabras reservadas, incluye palabras clave para:
# Tipos de datos, funciones y métodos built-in,
# declaración de variables, return statements,
# ciclos y condicionales
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
    'Print': 'PRINT',
    'Read': 'READ',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'SetPosition': 'SETPOSITION',
    'Translate': 'TRANSLATE',
    'SetControllable': 'SETCONTROLLABLE',
}

class LexerTudi(object):
    # Lista con los nombres de los tokens
    tokens = [
        'ASSIGN_OP', 'LOGIC_OPS', 'REL_OPS',
        'ID',
        'INT_LITERAL', 'FLOAT_LITERAL', 'BOOL_LITERAL', 'STRING_LITERAL']

    # Agrega el nombre de las palabras reservadas a la lista de tokens
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

    # Token para la operación de asignación
    t_ASSIGN_OP = '='

    # Expresión regular para los operadores relacionales
    def t_REL_OPS(self, t):
        r'<=|>=|>|<|!=|=='
        return t

    # Expresión regular para los operadores lógicos
    def t_LOGIC_OPS(self, t):
        r'\b(o|y)\b'
        return t

    # Expresión regular para identificar los literales booleanos (true o false)
    # El valor es casteado a la clase bool
    def t_BOOL_LITERAL(self, t):
        r'(true)|(false)'
        t.value = bool(t.value == 'true')
        return t

    # Expresión regular para identificar los identificadores para funciones y variables
    # Se checa si pertenece a las palabras reservadas para asignar el tipo correspondiente
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')
        return t

    # Expresión regular para identificar los literales string
    # Incluye caracteres alfanuméricos, espacios y caracteres específicos
    def t_STRING_LITERAL(self, t):
        r'\"(\w|\s|[-*+/():=])+\"'
        return t

    # Expresión regular para identificar los literales flotantes
    # El valor es casteado a la clase float
    def t_FLOAT_LITERAL(self, t):
        r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t

    # Expresión regular para identificar los literales enteros
    # El valor es casteado a la clase int
    def t_INT_LITERAL(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    # Expresión regular para darle seguimiento a los números de linea
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignore these chars (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0], t.lineno)
        raise Exception(f"Illegal character '{t.value[0]}' at line: {t.lineno}")

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
