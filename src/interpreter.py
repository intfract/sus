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
    
class Branch:
    def __init__(self, items) -> None:
        self.items = items
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.items}"

class Variable:
    def __init__(self, name: str, value) -> None:
        self.name: str = name
        self.value = value.value if isinstance(value, Variable) else value
    
    def __repr__(self):
        return f"var {self.name} -> {self.value}"

class Function:
    def __init__(self, name: str, params: list, body: Branch) -> None:
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"{self.name} ({self.params}) {self.body}"

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
            elif self.token.value == "[":
                temp.append(self.list())
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
            elif self.token.value == "(":
                temp.append(self.group())
            elif isinstance(self.token, Separator):
                items.append(copy.deepcopy(temp)) # prevents binding to self.token
                temp.clear()
            else:
                temp.append(copy.deepcopy(self.token))
            self.move()
        items.append(temp)
        return List(items)
    
    def branch(self):
        items = []
        self.move()
        while not self.end and self.token.value != "}":
            if self.token.value == "{":
                items.append(self.branch())
            elif self.token.value == "(":
                items.append(self.group())
            else:
                items.append(copy.deepcopy(self.token))
            self.move()
        return Branch(items)
    
    def build(self):
        while not self.end:
            if self.token.value == "(":
                self.tree.append(self.group())
            elif self.token.value == "[":
                self.tree.append(self.list())
            elif self.token.value == "{":
                self.tree.append(self.branch())
            else:
                self.tree.append(self.token)
            self.move()
        return self.tree

class Interpreter:
    def __init__(self, tree, memory) -> None:
        self.tree = tree
        self.index: int = 0
        self.node = self.tree[self.index]
        self.end: bool = False
        self.memory = memory
    
    def move(self):
        self.index += 1
        if self.index < len(self.tree):
            self.node = self.tree[self.index]
        else:
            self.end = True

    def execute(self, function: Function, args: list):
        memory = copy.deepcopy(self.memory)
        params = function.params
        if len(params) != len(args):
            raise ValueError(f"expected {params} arguments but got {args}")
        for i, param in enumerate(params):
            name = param.value
            memory[name] = args[i]
        print(memory)
    
    def simplify(self, expression):
        call = None
        if isinstance(expression, Reference):
            return self.memory[expression.value].value
        if isinstance(expression, (Integer, Float, Text)):
            return expression # standalone data
        for i, term in enumerate(expression):
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
                function = self.memory[call]
                if isinstance(function, Function):
                    self.execute(Function, term.items)
                else:
                    count = function.__code__.co_argcount
                    empty = count == 0 and len(term.items) == 1 and len(term.items[0]) == count
                    if len(term.items) != count and not empty:
                        raise ValueError(f"expected {count} arguments but got {len(term.items)}")
                    function = self.memory[call]
                    args = []
                    for arg in term.items:
                        args.append(self.simplify(arg))
                    return function() if empty else function(*args)
            elif isinstance(term, Group):
                if i == 0:
                    if len(term.items) != 1:
                        raise SyntaxError("function arguments in assignment") # arrow functions not supported yet
                    tokens = term.items[0]
                    return self.simplify(tokens)
            elif isinstance(term, List):
                if i == 0:
                    collection = List([])
                    for i, item in enumerate(term.items):
                        value = self.simplify(item)
                        if value is not None:
                            collection.items.append(item)
                    return collection

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
            if isinstance(self.node, (Integer, Float, Text)):
                self.memory[name] = Variable(name, self.node)
            elif isinstance(self.node, Block):
                if self.node.value == "func":
                    self.move()
                    if self.end or not isinstance(self.node, Group):
                        raise SyntaxError("expected function arguments")
                    args = []
                    if not (len(self.node.items) == 1 and len(self.node.items[0]) == 0): # not empty group
                        for i, item in enumerate(self.node.items):
                            if len(item) > 1 or not isinstance(item[0], Reference):
                                raise SyntaxError("expected parameter name")
                            args.append(item[0])
                    self.move()
                    if self.end or not isinstance(self.node, Branch):
                        raise SyntaxError("expected function body")
                    self.memory[name] = Function(name, args, copy.deepcopy(self.node))
            else:
                expression = [copy.deepcopy(self.node)]
                self.move()
                while not self.end and isinstance(self.node, (Group)):
                    expression.append(copy.deepcopy(self.node))
                    self.move()
                self.memory[name] = Variable(name, self.simplify(expression))

    def repeat(self, count):
        self.move()
        if not isinstance(self.node, Branch):
            raise SyntaxError("expected code block body")
        sub = Interpreter(self.node.items, self.memory)
        for i in range(count):
            new_memory = copy.deepcopy(sub.interpret())
            sub.memory = new_memory # updating memory before reset
            sub.index = 0
            sub.end = False
            sub.node = sub.tree[sub.index]
        self.memory = sub.memory

    def loop(self, condition):
        self.move()
        if not isinstance(self.node, Branch):
            raise SyntaxError("expected code block body")
        sub = Interpreter(self.node.items, self.memory)
        node = self.simplify([condition])
        condition_group = copy.deepcopy(condition)
        while node.value > 0:
            new_memory = copy.deepcopy(sub.interpret())
            sub.memory = new_memory # updating memory before reset
            evaluator = Interpreter([condition_group], new_memory)
            boolean = evaluator.simplify([condition_group])
            node.value = boolean.value
            sub.index = 0
            sub.end = False
            sub.node = sub.tree[sub.index]
        self.memory = sub.memory

    def interpret(self):
        while not self.end:
            if isinstance(self.node, Keyword):
                if (self.node.value == "set"):
                    self.handle_assignment()
            elif isinstance(self.node, Block):
                if self.node.value == "repeat":
                    self.move()
                    if (self.end):
                        raise SyntaxError("expected type Integer for repeat loop")
                    node = self.simplify([self.node])
                    if not isinstance(node, Integer):
                        raise SyntaxError(f"expected Integer not {node}")
                    self.repeat(node.value)
                if self.node.value == "while":
                    self.move()
                    if (self.end):
                        raise SyntaxError("expected type Integer for while loop")
                    self.loop(self.node)
            elif isinstance(self.node, Reference):
                expression = [copy.deepcopy(self.node)]
                self.move()
                while not self.end and isinstance(self.node, (Group)):
                    expression.append(copy.deepcopy(self.node))
                    self.move()
                if len(expression) > 1:
                    self.simplify(expression)
                else:
                    pass
            else:
                self.move()
        return self.memory