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
    
    def move(self):
        self.index += 1
        if self.index < len(self.tree):
            self.node = self.tree[self.index]
        else:
            self.end = True

    def interpret(self):
        pass