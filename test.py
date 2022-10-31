import unittest
import os

from parser_tudi import get_parser

class TestTUDI(unittest.TestCase):
    def setUp(self):
        self.folder = "test_cases"
        self.parser = get_parser()
    
    def test_declare_funcs(self):
        f = open(os.path.join(self.folder, "declare_funcs.tudi"), 'r')
        data = f.read()
        f.close()

        self.assertEqual(self.parser.parse(data), "Aceptado")


unittest.main()