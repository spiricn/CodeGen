from codegen.Token import *

class TextToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)