import unittest
import os

from lexer import LexerTudi
from parser_tudi import ParserTudi
from quadruples import Quadruple

class TestTUDI(unittest.TestCase):
    def setUp(self):
        self.folder = "test_cases"
        self.lexer = LexerTudi()
        self.lexer.build()

        self.parser = ParserTudi()
        self.parser.build(self.lexer)

    def get_quads_from_file(self, file_path):
        f = open(file_path, 'r')

        quads = []
        for count, line in enumerate(f):
            line = line.rstrip().split(sep=',')
            quads.append(Quadruple(count + 1, line[0], line[1], line[2], line[3]))
        f.close()

        return quads

    def test_tudi(self):
        f = open(os.path.join(self.folder, "test.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "test_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_basic_struct(self):
        f = open(os.path.join(self.folder, "basic_struct_empty.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "basic_struct_empty_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_declare_funcs(self):
        f = open(os.path.join(self.folder, "declare_funcs.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "declare_funcs_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")

    def test_declare_vars(self):
        f = open(os.path.join(self.folder, "declare_vars.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "declare_vars_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_call_funcs(self):
        f = open(os.path.join(self.folder, "call_funcs.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "call_funcs_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_call_methods(self):
        f = open(os.path.join(self.folder, "call_methods.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "call_methods_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")

    def test_conditional(self):
        f = open(os.path.join(self.folder, "conditional.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "conditional_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_loops(self):
        f = open(os.path.join(self.folder, "loops.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "loops_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")
    
    def test_assignment(self):
        f = open(os.path.join(self.folder, "assignment.tudi"), 'r')
        data = f.read()
        f.close()

        quads = self.get_quads_from_file(os.path.join(self.folder, "assignment_quads.txt"))

        self.assertEqual(self.parser.parse(data), "Aceptado")
        self.assertEqual(self.parser.quadruple_gen.quadruples, quads, "Quadruples are not the same")

unittest.main()