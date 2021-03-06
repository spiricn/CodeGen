from codegen.Token import *

class WhileLoopToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)
        
        self.condition = None
        
        if self.type == TOKEN_WHILE_LOOP_START:
            self.condition = self.body[len('<% while '):-3]