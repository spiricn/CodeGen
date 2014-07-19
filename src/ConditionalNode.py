from Node import *
from Token import *

class Condition(object):
    def __init__(self, token, node):
        self.token = token
        self.node = node
        
class ConditionalNode(Node):
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_CONDITIONAL)
        self.conditions = []
        
        current = tokens[0]
        
        tokens.pop(0)
        
        n = self.context.createContainer()
        
        processedEnd = False
        
        while not processedEnd:
            token = tokens[0]
            
            if current.type == TOKEN_CONDITIONAL_IF:
                if token.type in [TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_ELSE, TOKEN_CONDITIONAL_ELIF]:
                    processedEnd = (token.type == TOKEN_CONDITIONAL_END)
                    tokens.pop(0)
                    self.conditions.append( Condition(current, n) )
                    current = token
                    n = self.context.createContainer()
                else:
                    n.addChild(tokens)
            elif current.type == TOKEN_CONDITIONAL_ELIF:
                if token.type in [TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_ELSE]:
                    processedEnd = (token.type == TOKEN_CONDITIONAL_END)
                    tokens.pop(0)
                    self.conditions.append( Condition(current, n) )
                    current = token
                    n = self.context.createContainer()
                else:
                    n.addChild(tokens)
                    
            elif current.type == TOKEN_CONDITIONAL_ELSE:
                if token.type in [TOKEN_CONDITIONAL_END]:
                    processedEnd = True
                    tokens.pop(0)
                    self.conditions.append( Condition(current, n) )
                else:
                    n.addChild(tokens)
            else:
                n.addChild(tokens)
                
    def execute(self):
        passed = None
        
        for condition in self.conditions:
            if condition.token.type == TOKEN_CONDITIONAL_END:
                print('a')
                # None of the conditions passed
                break
            elif condition.token.type == TOKEN_CONDITIONAL_ELSE:
                # Reached else..
                passed = condition
                break
            # Evaluate a condition
            elif eval(condition.token.query, self.context.workspace):
                # Condition passed
                passed = condition
                break
            
        if passed == None:
            # Do nothing
            return
        
        # Execute body
        condition.node.execute()
    
    def __str__(self):
        return '<ConditionalNode>'