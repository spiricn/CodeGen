from codegen.Token import *

class CodeToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)
        
        self.inlineCode = None
        
        if self.type == TOKEN_CODE_START:
            code = self.body[len('<% code '):-3]
            
            if len(code):
                self.inlineCode = code
