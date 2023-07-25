import sys
from lib import add, floor, multiply, power, bool_and, bool_or, bool_xor, bool_not
from lexer import Lexer
from interpreter import Parser, Interpreter

def main():
    memory = {
        "add": add,
        "multiply": multiply,
        "power": power,
        "and": bool_and,
        "or": bool_or,
        "xor": bool_xor,
        "not": bool_not,
        "floor": floor,
    }
    file = sys.argv[1]
    if file is not None:
        with open(file, "r", encoding="utf8") as f:
            tokens = Lexer(f.read()).build()
            tree = Parser(tokens).build()
            output = Interpreter(tree, memory).interpret()
            print(output)
    code = input()
    tokens = Lexer(code).build()
    print(tokens)
    tree = Parser(tokens).build()
    print(tree)
    output = Interpreter(tree, memory).interpret()
    print(output)

main()