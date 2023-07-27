import sys
from lib import add, append, floor, get, multiply, pop, power, bool_and, bool_or, bool_xor, bool_not, sort, sus_print
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
        "get": get,
        "sort": sort,
        "append": append,
        "pop": pop,
        "print": sus_print,
    }
    if len(sys.argv) > 1:
        file = sys.argv[1]
        with open(file, "r", encoding="utf8") as f:
            tokens = Lexer(f.read()).build()
            tree = Parser(tokens).build()
            output = Interpreter(tree, memory).interpret()
            print(output)
    else:
        code = input()
        tokens = Lexer(code).build()
        # print(tokens)
        tree = Parser(tokens).build()
        # print(tree)
        output = Interpreter(tree, memory).interpret()
        print(output)

main()