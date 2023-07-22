from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator
import copy

class Group:
    def __init__(self, items) -> None:
        self.items = items
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.items}"

class List:
    def __init__(self, items) -> None:
        self.items = items
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.items}"

class Variable:
    def __init__(self, name: str, value) -> None:
        self.name: str = name
        self.value = value
    
    def __repr__(self):
        return f"var {self.name} -> {self.value}"

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index: int = 0
        self.token: Token = tokens[self.index]
        self.end: bool = False
        self.tree = []

    def move(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
        else:
            self.end = True

    def collapse(self):
        pass

    def group(self):
        items = []
        temp = []
        self.move()
        while not self.end and self.token.value != ")":
            if self.token.value == "(":
                temp.append(self.group())
            elif isinstance(self.token, Separator):
                items.append(copy.deepcopy(temp)) # prevents binding to self.token
                temp.clear()
            else:
                temp.append(copy.deepcopy(self.token))
            self.move()
        items.append(temp)
        return Group(items)
    
    def list(self):
        items = []
        temp = []
        self.move()
        while not self.end and self.token.value != "]":
            if self.token.value == "[":
                temp.append(self.list())
            elif isinstance(self.token, Separator):
                items.append(copy.deepcopy(temp)) # prevents binding to self.token
                temp.clear()
            else:
                temp.append(copy.deepcopy(self.token))
            self.move()
        items.append(temp)
        return List(items)
    
    def build(self):
        while not self.end:
            if self.token.value == "(":
                self.tree.append(self.group())
            elif self.token.value == "[":
                self.tree.append(self.list())
            else:
                self.tree.append(self.token)
            self.move()
        return self.tree

class Interpreter:
    def __init__(self, tree) -> None:
        self.tree = tree
        self.index: int = 0
        self.node = self.tree[self.index]
        self.end: bool = False
        self.memory = {}
    
    def move(self):
        self.index += 1
        if self.index < len(self.tree):
            self.node = self.tree[self.index]
        else:
            self.end = True
    
    def simplify(self, expression):
        call = None
        for i, term in enumerate(expression):
            print(term)
            if isinstance(term, Reference) and i == 0:
                if len(expression) == 1:
                    return self.memory[term.value].value # get variable value
                call = term.value
            elif isinstance(term, (Integer, Float, Text)) and len(expression) == 1:
                return term # standalone data
            elif call is not None:
                if not isinstance(term, Group):
                    raise SyntaxError("expected bracket group after function name")
                # call function from memory
            elif isinstance(term, Group):
                if i == 0:
                    if len(term.items) != 1:
                        raise SyntaxError("function arguments in assignment") # arrow functions not supported yet
                    tokens = term.items[0]
                    return self.simplify(tokens)

    def handle_assignment(self):
        # set x y to value
        var_names = []
        self.move()
        while not self.end and isinstance(self.node, Reference):
            var_names.append(self.node.value)
            self.move()
        if (len(var_names) == 0):
            raise SyntaxError("expected variable names")
        if (self.node.value != "to"):
            raise SyntaxError("expected \"to\" statement")
        self.move()
        if (not self.node):
            raise SyntaxError("empty assignment")
        for name in var_names:
            if (isinstance(self.node, (Integer, Float, Text))):
                self.memory[name] = Variable(name, self.node)
            else:
                expression = [copy.deepcopy(self.node)]
                self.move()
                while not self.end and isinstance(self.node, (Group)):
                    expression.append(copy.deepcopy(self.node))
                    self.move()
                self.memory[name] = Variable(name, self.simplify(expression))

    def interpret(self):
        while not self.end:
            if isinstance(self.node, Keyword):
                self.handle_assignment()
            self.move()
        return self.memory