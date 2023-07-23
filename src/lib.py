from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator
def add(x, y):
    if isinstance(x, Integer) and isinstance(y, Integer):
        return Integer(x + y)
    if isinstance(x, Float) or isinstance(y, Float):
        return Float(x + y)

def multiply(x, y):
    return Integer(x * y)