from codegen.Token import *

class FunctionToken(Token):
    def __init__(self, type, body, template, sourceLocation):
        Token.__init__(self, type, body, template, sourceLocation)

        self.params = None
        self.name = None
        self.numParams = 0
        
        if self.type in [TOKEN_FUNCTION_BEGIN, TOKEN_FUNCTION_CALL]:
            # Function params
            paramBegin = self.body.find('(')
            paramEnd = self.body.rfind(')')
            
            params = self.body[paramBegin+1:paramEnd]
            params = params.replace(' ', '').replace('\t', '')
            
            self.params = params.split(',')
            
            self.numParams = len(self.params)
            
            # Function name
            if self.type == TOKEN_FUNCTION_BEGIN:
                nameStart = len('<% function ')
            else:
                nameStart = len('<% call ')
                
            self.name = self.body[nameStart:].split('(')[0]
