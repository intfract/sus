class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"{self.__class__.__name__} {str(self.value)}"

class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)

class Float(Token):
    def __init__(self, value):
        super().__init__("FLT", value)

class Text(Token):
    def __init__(self, value):
        super().__init__("TXT", value)

class Reference(Token):
    def __init__(self, value):
        super().__init__("REF", value)

class Keyword(Token):
    def __init__(self, value):
        super().__init__("KEY", value)

class Block(Token):
    def __init__(self, value):
        super().__init__("BLK", value)

class Open(Token):
    def __init__(self, value):
        super().__init__("OPN", value)

class Close(Token):
    def __init__(self, value):
        super().__init__("CLS", value)