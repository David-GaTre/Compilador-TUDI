from cmath import exp


data_types = {
    'int': 'int',
    'float': 'float',
    'char': 'char',
    'bool': 'bool',
    'arr1d': 'arr1d',
}

class sem_cube:
    valid_ops = {
        # Int - Int
        '+,II': data_types['int'],
        '-,II': data_types['int'],
        '*,II': data_types['int'],
        '/,II': data_types['float'],
        '>,II': data_types['bool'],
        '>=,II': data_types['bool'],
        '==,II': data_types['bool'],
        '!=,II': data_types['bool'],
        '<,II': data_types['bool'],
        '<=,II': data_types['bool'],
        'y,II': data_types['bool'],
        'o,II': data_types['bool'],
        # Int - Float
        '+,IF': data_types['float'],
        '-,IF': data_types['float'],
        '*,IF': data_types['float'],
        '/,IF': data_types['float'],
        '>,IF': data_types['bool'],
        '>=,IF': data_types['bool'],
        '==,IF': data_types['bool'],
        '!=,IF': data_types['bool'],
        '<,IF': data_types['bool'],
        '<=,IF': data_types['bool'],
        'y,IF': data_types['bool'],
        'o,IF': data_types['bool'],
        # Int - Bool
        '+,IB': data_types['int'],
        '-,IB': data_types['int'],
        '*,IB': data_types['int'],
        '/,IB': data_types['float'],
        '>,IB': data_types['bool'],
        '>=,IB': data_types['bool'],
        '==,IB': data_types['bool'],
        '!=,IB': data_types['bool'],
        '<,IB': data_types['bool'],
        '<=,IB': data_types['bool'],
        'y,IB': data_types['bool'],
        'o,IB': data_types['bool'],
        # Float - Float
        '+,FF': data_types['float'],
        '-,FF': data_types['float'],
        '*,FF': data_types['float'],
        '/,FF': data_types['float'],
        '>,FF': data_types['bool'],
        '>=,FF': data_types['bool'],
        '==,FF': data_types['bool'],
        '!=,FF': data_types['bool'],
        '<,FF': data_types['bool'],
        '<=,FF': data_types['bool'],
        'y,FF': data_types['bool'],
        'o,FF': data_types['bool'],
        # Float - Bool
        '+,FB': data_types['float'],
        '-,FB': data_types['float'],
        '*,FB': data_types['float'],
        '/,FB': data_types['float'],
        '>,FB': data_types['bool'],
        '>=,FB': data_types['bool'],
        '==,FB': data_types['bool'],
        '!=,FB': data_types['bool'],
        '<,FB': data_types['bool'],
        '<=,FB': data_types['bool'],
        'y,FB': data_types['bool'],
        'o,FB': data_types['bool'],
        # Char - Char
        '+,CC': data_types['arr1d'], # Like a C string
        '>,CC': data_types['bool'],
        '>=,CC': data_types['bool'],
        '==,CC': data_types['bool'],
        '!=,CC': data_types['bool'],
        '<,CC': data_types['bool'],
        '<=,CC': data_types['bool'],
        'y,CC': data_types['bool'],
        'o,CC': data_types['bool'],
        # Bool - Int
        '+,BI': data_types['int'],
        '-,BI': data_types['int'],
        '*,BI': data_types['int'],
        '/,BI': data_types['float'],
        '>,BI': data_types['bool'],
        '>=,BI': data_types['bool'],
        '==,BI': data_types['bool'],
        '!=,BI': data_types['bool'],
        '<,BI': data_types['bool'],
        '<=,BI': data_types['bool'],
        'y,BI': data_types['bool'],
        'o,BI': data_types['bool'],
        # Bool - Float
        '+,BF': data_types['float'],
        '-,BF': data_types['float'],
        '*,BF': data_types['float'],
        '/,BF': data_types['float'],
        '>,BF': data_types['bool'],
        '>=,BF': data_types['bool'],
        '==,BF': data_types['bool'],
        '!=,BF': data_types['bool'],
        '<,BF': data_types['bool'],
        '<=,BF': data_types['bool'],
        'y,BF': data_types['bool'],
        'o,BF': data_types['bool'],
        # Bool Bool
        '+,BF': data_types['float'],
        '-,BF': data_types['float'],
        '*,BF': data_types['float'],
        '/,BF': data_types['float'],
        '>,BF': data_types['bool'],
        '>=,BF': data_types['bool'],
        '==,BF': data_types['bool'],
        '!=,BF': data_types['bool'],
        '<,BF': data_types['bool'],
        '<=,BF': data_types['bool'],
        'y,BF': data_types['bool'],
        'o,BF': data_types['bool'],
        # Array1d - Array1d
        '+,AA': data_types['arr1d']
    }

    def exp(self, left_ope:str, right_ope:str, operator:str):
        return operator + ',' + left_ope + right_ope

    def validate_exp(self, left_ope:str, right_ope:str, operator:str):
        expression = exp(left_ope, right_ope, operator)
        if expression in self.valid_ops.keys():
            return self.valid_ops[expression]
        else:
            return "ERROR: Not valid operation"