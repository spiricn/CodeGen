from codegen.Token import *

class ConditionalToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)
        
        self.query = None
        
        if self.type == TOKEN_CONDITIONAL_IF:
            self.query = body[len('<% if '):-3]
        elif self.type == TOKEN_CONDITIONAL_ELIF:
            self.query = body[len('<% elif '):-3] 