from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close

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
        self.move()
        while not self.end and self.token.value != ")":
            if self.token.value == "(":
                items.append(self.group())
            else:
                items.append(self.token)
            self.move()
        return items
    
    def build(self):
        while not self.end:
            if self.token.value == "(":
                items = self.group()
                print(f"group: {items}")
            self.move()