# Possible node types
NODE_TEXT, \
NODE_CODE, \
NODE_CONDITIONAL, \
NODE_EVAL, \
NODE_LOOP, \
NODE_CONTAINER, \
NODE_WHILE_LOOP, \
= range(7)

class Node(object):
    '''
    Generic Node interface which is used as a base class for all other objects
    '''
    
    def __init__(self, context, type):
        self.context = context
        self.type = type
    
    def execute(self):
        raise NotImplementedError("Node execute method not implemented")
    