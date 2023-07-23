from lib import add, multiply
from lexer import Lexer
from interpreter import Parser, Interpreter

def main():
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