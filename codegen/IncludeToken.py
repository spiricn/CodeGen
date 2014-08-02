from codegen.Token import *

class IncludeToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)

        self.file = body[len('<% include '):-3]