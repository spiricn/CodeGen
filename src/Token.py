TOKEN_INVALID,          \
TOKEN_TEXT,             \
TOKEN_CODE_START,       \
TOKEN_CODE_END,         \
TOKEN_EVAL,             \
TOKEN_CONDITIONAL_IF,   \
TOKEN_CONDITIONAL_ELIF, \
TOKEN_CONDITIONAL_ELSE, \
TOKEN_CONDITIONAL_END,  \
TOKEN_FOR_LOOP_START,       \
TOKEN_FOR_LOOP_END,         \
TOKEN_INCLUDE,          \
TOKEN_WHILE_LOOP_START,      \
TOKEN_WHILE_LOOP_END,        \
= range(14)

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
         TOKEN_FOR_LOOP_START : 'FOR_LOOP_START',
         TOKEN_FOR_LOOP_END : 'FOR_LOOP_END',
         TOKEN_INCLUDE : 'INCLUDE',
         TOKEN_WHILE_LOOP_START : 'WHILE_LOOP_START',
         TOKEN_WHILE_LOOP_END : 'WHILE_LOOP_END',
         
        }[self.type]
         
    def __str__(self):
        return '<Token %s>' % self.getTypeName()
