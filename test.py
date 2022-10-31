import unittest
import os

from parser_tudi import get_parser

class TestTUDI(unittest.TestCase):
    def setUp(self):
        self.folder = "test_cases"
        self.parser = get_parser()

    def tearDown(self):
        self.parser.restart()

    def test_tudi(self):
        f = open(os.path.join(self.folder, "test.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_basic_struct(self):
        f = open(os.path.join(self.folder, "basic_struct_empty.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_declare_funcs(self):
        f = open(os.path.join(self.folder, "declare_funcs.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")

    def test_declare_vars(self):
        f = open(os.path.join(self.folder, "declare_vars.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_call_funcs(self):
        f = open(os.path.join(self.folder, "call_funcs.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_call_methods(self):
        f = open(os.path.join(self.folder, "call_methods.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")

    def test_conditional(self):
        f = open(os.path.join(self.folder, "conditional.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_loops(self):
        f = open(os.path.join(self.folder, "loops.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")
    
    def test_assignment(self):
        f = open(os.path.join(self.folder, "assignment.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")

unittest.main()