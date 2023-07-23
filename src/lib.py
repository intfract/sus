from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator

def restrict_bool(*args):
    for arg in args:
        if (arg not in (0, 1)):
            raise TypeError("boolean arguments must be bit type")

def add(x, y):
    if isinstance(x, Integer) and isinstance(y, Integer):
        return Integer(x + y)
    if isinstance(x, Float) or isinstance(y, Float):
        return Float(x + y)

def multiply(x, y):
    if isinstance(x, Integer) and isinstance(y, Integer):
        return Integer(x * y)
    if isinstance(x, Float) or isinstance(y, Float):
        return Float(x * y)

def bool_and(x, y):
    x = int(x.value)
    y = int(y.value)
    restrict_bool(x, y)
    return Integer(int(x and y))

def bool_or(x, y):
    x = int(x.value)
    y = int(y.value)
    restrict_bool(x, y)
    return Integer(int(x or y))

def bool_xor(x, y):
    x = int(x.value)
    y = int(y.value)
    restrict_bool(x, y)
    return Integer(int((x and not y) or (not x and y)))

def bool_not(x):
    x = int(x.value)
    restrict_bool(x)
    return Integer(int(not x))