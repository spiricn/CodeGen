from ContainerNode import *
from Token import *

class ForLoopNode(Node):
    '''
    Node representing a for loop.
    '''
    
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_LOOP)
        
        # Token describin the loop start (i.e. <% for a in b >)
        self.loop = tokens.pop(0)
        
        # Node representing a loop body
        n = self.context.createContainer()
    
        # Find the loop end, and generate a body    
        while len(tokens):
            token = tokens[0]
            
            if token.type == TOKEN_FOR_LOOP_END:
                # Found the end
                tokens.pop(0)
                break
            else:
                n.addChild(tokens)
                
        self.body = n
        
    def execute(self, locals):
        # List of loop variables (i.e. in <% for a,b,c in D > the list will be ['a','b','c'])
        varList = self.loop.vars.split(',')
         
        loopCode = ''
        
        # Create loop header
        loopCode += 'for %s in eval("%s", self.context.workspace, locals):\n' % (self.loop.vars, self.loop.container)
        
        # Expose loop variables
        for var in varList:
            loopCode += "\tlocals['%s'] = %s\n" % (var, var) 
     
        # Loop body execution code
        loopCode += '\tself.body.execute(locals)'


        # Execute the loop        
        try:
            exec(loopCode)
        except Exception as e:
            # Failed executing loop
            print('Error executing loop; reason %s; loop =\"%s\"' % (e, loopCode))
