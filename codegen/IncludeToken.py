from codegen.Token import *

class IncludeToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)

        self.file = body[len('<% include '):-3]