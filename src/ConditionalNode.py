from Node import *
from Token import *

class Condition(object):
    def __init__(self, token, node):
        self.token = token
        self.node = node

class ConditionalNode(Node):
    '''
    Node presenting a conditional expression (if, elif and else pairs)
    '''
    
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_CONDITIONAL)
        self.conditions = []
        
        conditionHeader = tokens[0]
        
        tokens.pop(0)
        
        conditionBody = self.context.createContainer()
        
        processedEnd = False
        
        while not processedEnd:
            token = tokens[0]
            
            conditionEnd = False
            if conditionHeader.type == TOKEN_CONDITIONAL_IF and token.type in [TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_ELSE, TOKEN_CONDITIONAL_ELIF]:
                conditionEnd = True
                processedEnd = (token.type == TOKEN_CONDITIONAL_END)
                    
            elif conditionHeader.type == TOKEN_CONDITIONAL_ELIF and token.type in [TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_ELSE]:
                processedEnd = (token.type == TOKEN_CONDITIONAL_END)
                conditionEnd = True
                    
            elif conditionHeader.type == TOKEN_CONDITIONAL_ELSE and token.type in [TOKEN_CONDITIONAL_END]:
                processedEnd = True
                conditionEnd = True
                
            if conditionEnd:
                # Reached condition end
                tokens.pop(0)
                self.conditions.append( Condition(conditionHeader, conditionBody) )
                
                # New header and body
                conditionHeader = token
                conditionBody = self.context.createContainer()
            else:
                # Consume condition body
                conditionBody.addChild( tokens )

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