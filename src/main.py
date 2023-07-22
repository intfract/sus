from lexer import Lexer
from interpreter import Parser

code = input()

tokens = Lexer(code).build()
print(tokens)
tree = Parser(tokens).build()
print(tree)