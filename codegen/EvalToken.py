from codegen.Token import *

class EvalToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
        self.expression = self.body[len('<= '):-3] 