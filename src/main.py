from lexer import Lexer
from interpreter import Parser

code = input()

tokens = Lexer(code).build()
print(tokens)
Parser(tokens).build()