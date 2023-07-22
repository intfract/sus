from tokens import Token, Integer, Float, Text, Reference, Keyword, Block, Open, Close, Separator
import math

class Lexer:
    digits = '0123456789'
    letters = "abcdefghijklmnopqrstuvwxyz_"
    quotes = "\"'"
    ignore = ["\n", "\t", " "]
    separator = ","

    def __init__(self, code) -> None:
        self.code = code
        self.index: int = 0
        self.tokens = []
        self.char = self.code[self.index]
        self.token: Token = None
        self.end: bool = False
        self.keywords = ["set", "to", "return"]
        self.blocks = ["if", "while"]
        self.brackets = ["(", ")", "[", "]", "{", "}"]
        self.scales = [0] * (len(self.brackets) // 2)
    
    def move(self):
        self.index += 1
        if self.index < len(self.code):
            self.char = self.code[self.index]
        else:
            self.end = True

    def extract_number(self):
        number = ""
        isFloat = False
        while (self.char in self.digits or self.char == ".") and (not self.end):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()
        
        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ""
        while self.char.lower() in self.letters and not self.end:
            word += self.char
            self.move()
        
        return word
    
    def build(self):
        while not self.end:
            self.token = ""
            if self.char in self.ignore:
                self.move()
                continue

            if self.char in self.digits:
                self.token = self.extract_number()
            elif self.char.lower() in self.letters:
                word = self.extract_word()
                if word in self.keywords:
                    self.token = Keyword(word)
                elif word in self.blocks:
                    self.token = Block(word)
                else:
                    self.token = Reference(word)
            elif self.char in self.quotes:
                begin = self.char
                string = ""
                self.move()
                while not self.end and self.char != begin:
                    string += self.char
                self.token = Text(string)
                self.move()
            elif self.char in self.brackets:
                i = self.brackets.index(self.char)
                is_open = i % 2 == 0
                self.scales[math.floor(i / 2)] += 1 if is_open else -1
                if self.scales[math.floor(i / 2)] < 0:
                    raise SyntaxError()
                self.token = Open(self.char) if is_open else Close(self.char)
                self.move()
            elif self.char == self.separator:
                self.token = Separator(self.char)
                self.move()
            else:
                # handle illegal character
                pass
            
            print(self.token)
            self.tokens.append(self.token)

        if sum(self.scales) != 0:
            raise SyntaxError(self.scales)
        return self.tokens
