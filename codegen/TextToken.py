from codegen.Token import *

class TextToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)