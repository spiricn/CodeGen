from codegen.Node import *
from codegen.Token import *
import traceback
import sys

class EvalNode(Node):
    '''
    Node representing an evaluation expression.
    '''
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_EVAL)
        
        # We only need the first token
        self.token = tokens.pop(0)
        
        # Sanity check
        assert(self.token.type == TOKEN_EVAL)
        
    def execute(self, locals):
        try:
            # Try to evaluate the expression
            self.context.write( str( eval(self.token.expression, self.context.workspace, locals) ) )
        except Exception as e:
            # Expression could not be evalulated
            print('Error evaluating expression "%s"; reason: %s' % (self.token.expression, e))
            traceback.print_exc(file=sys.stdout)
            raise
        
    def __str__(self):
        return '<EvalNode>'
                