from codegen.Token import *

class EvalToken(Token):
    def __init__(self, type, body, template,sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)
        
        self.expression = self.body[len('<= '):-3] 