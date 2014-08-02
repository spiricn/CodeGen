from codegen.Token import *

class ForLoopToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)
        
        self.vars = None
        self.container = None
        
        if self.type == TOKEN_FOR_LOOP_START:
            loop = self.body[len('<% for '):-3]
            
            self.vars = loop.split(' in ')[0].replace(' ', '')
        
            self.container = loop.split(' in ')[1]