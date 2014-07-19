from Utils import *

TOKEN_INVALID,          \
TOKEN_TEXT,             \
TOKEN_CODE_START,       \
TOKEN_CODE_END,         \
TOKEN_EVAL,             \
TOKEN_CONDITIONAL_IF,   \
TOKEN_CONDITIONAL_ELIF, \
TOKEN_CONDITIONAL_ELSE, \
TOKEN_CONDITIONAL_END,  \
TOKEN_LOOP_START,       \
TOKEN_LOOP_END,         \
TOKEN_INCLUDE,          \
= range(12)

class Token(object):
    def __init__(self, type, body):
        self.type = type
        self.body = body
        
    def getTypeName(self):
        return {
         TOKEN_INVALID : 'INVALID',
         TOKEN_TEXT : 'TEXT',
         TOKEN_CODE_START : 'CODE_START',
         TOKEN_CODE_END : 'CODE_END',
         TOKEN_EVAL : 'EVAL',
         TOKEN_CONDITIONAL_IF : 'CONDITIONAL_IF',
         TOKEN_CONDITIONAL_ELIF : 'CONDITIONAL_ELIF',
         TOKEN_CONDITIONAL_ELSE : 'CONDITIONAL_ELSE',
         TOKEN_CONDITIONAL_END : 'CONDITIONAL_END',
         TOKEN_LOOP_START : 'LOOP_START',
         TOKEN_LOOP_END : 'LOOP_END',
         TOKEN_INCLUDE : 'INCLUDE'
        }[self.type]
         
    def __str__(self):
        return '<Token %s>' % self.getTypeName()


class ConditionalToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
        self.query = None
        
        if self.type == TOKEN_CONDITIONAL_IF:
            self.query = body[len('<% if '):-3]
        elif self.type == TOKEN_CONDITIONAL_ELIF:
            self.query = body[len('<% elif '):-3] 
                   
class TextToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
class CodeToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
class LoopToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
        self.vars = None
        self.container = None
        
        if self.type == TOKEN_LOOP_START:
            loop = self.body[len('<% for '):-3]
            
            self.vars = loop.split(' in ')[0].replace(' ', '')
        
            self.container = loop.split(' in ')[1]
        
class EvalToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)
        
        self.expression = self.body[len('<= '):-3] 
        
class IncludeToken(Token):
    def __init__(self, type, body):
        Token.__init__(self, type, body)

        self.file = body[len('<% include '):-3]
