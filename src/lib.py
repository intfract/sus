from interpreter import List
import math
from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator

def restrict_bool(*args):
    for arg in args:
        if (arg not in (0, 1)):
            raise TypeError("boolean arguments must be bit type")

def add(x, y):
    if isinstance(x, Integer) and isinstance(y, Integer):
        return Integer(x + y)
    if isinstance(x, (Integer, Float)) and isinstance(y, (Integer, Float)):
        return Float(x + y)
    raise TypeError("expected Integer or Float")

def multiply(x, y):
    if isinstance(x, Integer) and isinstance(y, Integer):
        return Integer(x * y)
    if isinstance(x, (Integer, Float)) and isinstance(y, (Integer, Float)):
        return Float(x * y)
    raise TypeError("expected Integer or Float")

def power(x, y):
    if isinstance(x, (Integer, Float)) and isinstance(y, (Integer, Float)):
        return Float(pow(x.value, y.value))
    raise TypeError("expected Integer or Float")

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

def floor(x):
    if isinstance(x, (Integer, Float)):
        return Float(math.floor(x.value))
    raise TypeError("expected Integer or Float")

def get(collection, index):
    if isinstance(index, Integer):
        index = index.value
    if isinstance(collection, List):
        return collection.items[index]
    
def sort(collection):
    if isinstance(collection, List):
        collection.items.sort()
        return collection
    
def append(collection, item):
    if isinstance(collection, List):
        collection.items.append(item)
        return collection

def pop(collection, index):
    if isinstance(index, Integer):
        index = index.value
    if isinstance(collection, List):
        return collection.items.pop(index)
    
def output(x: Token):
    print(x.value)

def sus_input(x):
    y = input()
    if isinstance(x, Integer):
        return Integer(y)
    if isinstance(x, Float):
        return Float(y)
    return Text(y)

def read(path: Text):
    if not isinstance(path, Text):
        raise TypeError("path must be Text")
    with open(path.value, "r", encoding="utf8") as f:
        return Text(f.read())

def write(path: Text, content: Text):
    if not isinstance(path, Text):
        raise TypeError("path must be Text")
    with open(path.value, "w") as f:
        f.write(content.value)