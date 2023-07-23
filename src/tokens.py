class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"{self.__class__.__name__} \033[94m{str(self.value)}\033[0m"

class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)
    
    def __add__(self, other):
        if isinstance(other, Integer):
            return int(self.value) + int(other.value)
        return int(self.value) + other
    
    def __mul__(self, other):
        if isinstance(other, Integer):
            return int(self.value) * int(other.value)
        return int(self.value) * other

class Float(Token):
    def __init__(self, value):
        super().__init__("FLT", value)
    
    def __add__(self, other):
        if isinstance(other, Float):
            return float(self.value) + float(other.value)
        return float(self.value) + other
    
    def __mul__(self, other):
        if isinstance(other, Float):
            return float(self.value) * float(other.value)
        return float(self.value) * other

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

class Separator(Token):
    def __init__(self, value):
        super().__init__("SEP", value)