INT = 'int'
FLOAT = 'float'
CHAR = 'char'
BOOL = 'bool'
ARR1D = 'arr1d'

class SemanticCube:
    valid_expressions = {
        # Int - Int
        '+,II': INT,
        '-,II': INT,
        '*,II': INT,
        '/,II': FLOAT,
        '>,II': BOOL,
        '>=,II': BOOL,
        '==,II': BOOL,
        '!=,II': BOOL,
        '<,II': BOOL,
        '<=,II': BOOL,
        'y,II': BOOL,
        'o,II': BOOL,
        # Int - Float
        '+,IF': FLOAT,
        '-,IF': FLOAT,
        '*,IF': FLOAT,
        '/,IF': FLOAT,
        '>,IF': BOOL,
        '>=,IF': BOOL,
        '==,IF': BOOL,
        '!=,IF': BOOL,
        '<,IF': BOOL,
        '<=,IF': BOOL,
        'y,IF': BOOL,
        'o,IF': BOOL,
        # Int - Bool
        '+,IB': INT,
        '-,IB': INT,
        '*,IB': INT,
        '/,IB': FLOAT,
        '>,IB': BOOL,
        '>=,IB': BOOL,
        '==,IB': BOOL,
        '!=,IB': BOOL,
        '<,IB': BOOL,
        '<=,IB': BOOL,
        'y,IB': BOOL,
        'o,IB': BOOL,
        # Float - Int
        '+,FI': FLOAT,
        '-,FI': FLOAT,
        '*,FI': FLOAT,
        '/,FI': FLOAT,
        '>,FI': BOOL,
        '>=,FI': BOOL,
        '==,FI': BOOL,
        '!=,FI': BOOL,
        '<,FI': BOOL,
        '<=,FI': BOOL,
        'y,FI': BOOL,
        'o,FI': BOOL,
        # Float - Float
        '+,FF': FLOAT,
        '-,FF': FLOAT,
        '*,FF': FLOAT,
        '/,FF': FLOAT,
        '>,FF': BOOL,
        '>=,FF': BOOL,
        '==,FF': BOOL,
        '!=,FF': BOOL,
        '<,FF': BOOL,
        '<=,FF': BOOL,
        'y,FF': BOOL,
        'o,FF': BOOL,
        # Float - Bool
        '+,FB': FLOAT,
        '-,FB': FLOAT,
        '*,FB': FLOAT,
        '/,FB': FLOAT,
        '>,FB': BOOL,
        '>=,FB': BOOL,
        '==,FB': BOOL,
        '!=,FB': BOOL,
        '<,FB': BOOL,
        '<=,FB': BOOL,
        'y,FB': BOOL,
        'o,FB': BOOL,
        # Char - Char
        '+,CC': ARR1D, # Like a C string
        '>,CC': BOOL,
        '>=,CC': BOOL,
        '==,CC': BOOL,
        '!=,CC': BOOL,
        '<,CC': BOOL,
        '<=,CC': BOOL,
        'y,CC': BOOL,
        'o,CC': BOOL,
        # Bool - Int
        '+,BI': INT,
        '-,BI': INT,
        '*,BI': INT,
        '/,BI': FLOAT,
        '>,BI': BOOL,
        '>=,BI': BOOL,
        '==,BI': BOOL,
        '!=,BI': BOOL,
        '<,BI': BOOL,
        '<=,BI': BOOL,
        'y,BI': BOOL,
        'o,BI': BOOL,
        # Bool - Float
        '+,BF': FLOAT,
        '-,BF': FLOAT,
        '*,BF': FLOAT,
        '/,BF': FLOAT,
        '>,BF': BOOL,
        '>=,BF': BOOL,
        '==,BF': BOOL,
        '!=,BF': BOOL,
        '<,BF': BOOL,
        '<=,BF': BOOL,
        'y,BF': BOOL,
        'o,BF': BOOL,
        # Bool - Bool
        '+,BB': INT,
        '-,BB': INT,
        '*,BB': INT,
        '/,BB': FLOAT,
        '>,BB': BOOL,
        '>=,BB': BOOL,
        '==,BB': BOOL,
        '!=,BB': BOOL,
        '<,BB': BOOL,
        '<=,BB': BOOL,
        'y,BB': BOOL,
        'o,BB': BOOL,
        # Array1d - Array1d
        '+,AA': ARR1D
    }

    def create_operation(self, left_operand: str, right_operand: str, operator: str):
        return operator + ',' + left_operand + right_operand

    def validate_operation(self, left_operand: str, right_operand: str, operator: str):
        expression = self.create_operation(left_operand, right_operand, operator)
        return self.valid_expressions.get(expression, "ERROR: Not valid operation")