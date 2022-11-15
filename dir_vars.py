from typing import Tuple, Dict

class VariablesTable:
    def __init__(self):
        self.table = {}

    def add_variable(self, name: str, var_type: str, mem: int) -> bool:
        if name in self.table:
            return False

        self.table[name] = {'type': var_type, 'address': mem}
        return True

    def get_variable(self, name: str) -> Tuple[bool, Dict]:
        if name not in self.table:
            return False, {}

        return True, self.table[name]
    
    def set_variable_value(self, name: str, value, mem: int) -> bool:
        if name not in self.table:
            return False

        self.table[name].update({'value': value})
        return True

class FunctionsDirectory:
    def __init__(self):
        self.GLOBAL_ENV = '0'
        self.directory = {}
        self.directory[self.GLOBAL_ENV] = {'table': VariablesTable()}

    def add_function(self, func_name: str, return_type: str, start: int) -> bool:
        if func_name in self.directory:
            return False

        self.directory[func_name] = {'start': start, 'return_type': return_type, 'params': [], 'table': VariablesTable()}
        return True

    def add_param(self, func_name: str, var_name: str, var_type: str, mem: int) -> bool:
        if func_name not in self.directory:
            return False
        
        if not self.add_variable(func_name, var_name, var_type, mem):
            return False

        self.directory[func_name]['params'].append((var_type, var_name, mem))
        return True

    def add_variable(self, func_name: str, var_name: str, var_type: str, mem: int) -> bool:
        if func_name not in self.directory:
            return False

        return self.directory[func_name]['table'].add_variable(var_name, var_type, mem)

    def set_variable(self, func_name: str, var_name: str, value, mem: int) -> bool:
        if func_name not in self.directory:
            return False
        
        if not self.directory[func_name]['table'].set_variable_value(var_name, value, mem):
            return False

        return self.set_variable(var_name, value)

    def find_variable(self, func_name: str, var_name: str) -> Dict:
        if func_name not in self.directory:
            return {}
        
        found, var_table = self.directory[func_name]['table'].get_variable(var_name)
        if found:
            return var_table

        _, var_table = self.directory[self.GLOBAL_ENV]['table'].get_variable(var_name)
        return var_table

    def find_function(self, func_name: str) -> Dict:
        if func_name not in self.directory:
            return {}

        return self.directory[func_name]