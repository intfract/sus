from lexer import Lexer
from interpreter import Parser, Interpreter

code = input()

tokens = Lexer(code).build()
print(tokens)
tree = Parser(tokens).build()
print(tree)
output = Interpreter(tree).interpret()
print(output)