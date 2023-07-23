from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator
from lexer import Lexer
from interpreter import Parser, Interpreter

def main():
    def add(x, y):
        if isinstance(x, Integer) and isinstance(y, Integer):
            return Integer(x + y)
        if isinstance(x, Float) or isinstance(y, Float):
            return Float(x + y)
    def multiply(x, y):
        return Integer(x * y)
    memory = {
        "add": add,
        "multiply": multiply,
    }
    code = input()
    tokens = Lexer(code).build()
    print(tokens)
    tree = Parser(tokens).build()
    print(tree)
    output = Interpreter(tree, memory).interpret()
    print(output)

main()