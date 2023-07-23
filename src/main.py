from lib import add, multiply, bool_and, bool_or, bool_xor, bool_not
from lexer import Lexer
from interpreter import Parser, Interpreter

def main():
    memory = {
        "add": add,
        "multiply": multiply,
        "and": bool_and,
        "or": bool_or,
        "xor": bool_xor,
        "not": bool_not,
    }
    code = input()
    tokens = Lexer(code).build()
    print(tokens)
    tree = Parser(tokens).build()
    print(tree)
    output = Interpreter(tree, memory).interpret()
    print(output)

main()