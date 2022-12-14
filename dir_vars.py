from typing import Tuple, Dict, List
from memory import type_to_char, get_default

class VariablesTable:
    def __init__(self):
        self.table = {}

    def add_variable(self, name: str, var_type: str, mem: int, dims: List[Tuple], length=1) -> bool:
        if name in self.table:
            return False

        self.table[name] = {'type': var_type, 'address': mem, 'dims': dims, 'length': length}
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

        self.directory[func_name] = {'start': start, 'return_type': return_type, 'params': [], 'table': VariablesTable(), 'return_address': None}
        return True

    def add_return_address(self, func_name: str, return_address: int) -> bool:
        if func_name not in self.directory:
            return False

        self.directory[func_name]['return_address'] = return_address
        return True

    def add_resources(self, func_name: str, resources: Dict) -> bool:
        if func_name not in self.directory:
            return False

        self.directory[func_name]['resources'] = resources
        return True

    def add_param(self, func_name: str, var_name: str, var_type: str, mem: int, dims: List[Tuple]) -> bool:
        if func_name not in self.directory:
            return False
        
        if not self.add_variable(func_name, var_name, var_type, mem, dims[1], dims[0]):
            return False

        dims_params = [dims[0]]
        if dims[1] is not None:
            for dim in dims[1]:
                dims_params.append(dim[0])
        else:
            dims_params.append(dims[1])
        dims_params = tuple(dims_params)

        self.directory[func_name]['params'].append((var_type, var_name, mem, dims_params))
        return True

    def add_variable(self, func_name: str, var_name: str, var_type: str, mem: int, dims: List[Tuple], length=1) -> bool:
        if func_name not in self.directory:
            return False

        return self.directory[func_name]['table'].add_variable(var_name, var_type, mem, dims, length)

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

    def clear_var_table(self, func_name: str):
        if func_name in self.directory:
            self.directory[func_name]['table'] = VariablesTable()

    def get_global_mem(self):
        global_mem = dict()
        # "Allocate" recursos para la memoria global
        for k, v in self.directory[self.GLOBAL_ENV]['table'].table.items():
            for i in range(v["length"]):
                global_mem[v["address"] + i] = get_default(type_to_char[v["type"]])
        return global_mem
