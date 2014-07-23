from Node import *
from TextNode import TextNode
from CodeNode import CodeNode
from ConditionalNode import ConditionalNode
from EvalNode import EvalNode
from ForLoopNode import ForLoopNode
from WhileLoopNode import WhileLoopNode
from FunctionDefNode import FunctionDefNode
from FunctionCallNode import FunctionCallNode 
from Token import *

class ContainerNode(Node):
    '''
    A node containing multiple child nodes of various types
    '''
    
    def __init__(self, context):
        Node.__init__(self, context, NODE_CONTAINER)
        
        self.children = []
        
            
    def execute(self, locals={}):
        for child in self.children:
            child.execute(locals)
            
    def createChildren(self, tokens):
        while len(tokens):
            self.addChild(tokens)

    def addChild(self, tokens):
        token = tokens[0]
             
        if token.type == TOKEN_TEXT:
            self.children.append( TextNode(self.context, tokens) )
            
        elif token.type == TOKEN_CODE_START:
            self.children.append( CodeNode(self.context, tokens) )
            
        elif token.type == TOKEN_CONDITIONAL_IF:
            self.children.append( ConditionalNode(self.context, tokens) )
            
        elif token.type == TOKEN_EVAL:
            self.children.append( EvalNode(self.context, tokens) )
            
        elif token.type == TOKEN_FOR_LOOP_START:
            self.children.append( ForLoopNode(self.context, tokens) )
            
        elif token.type == TOKEN_WHILE_LOOP_START:
            self.children.append( WhileLoopNode(self.context, tokens) )
            
        elif token.type == TOKEN_FUNCTION_BEGIN:
            self.children.append( FunctionDefNode(self.context, tokens) )
            
        elif token.type == TOKEN_FUNCTION_CALL:
            self.children.append( FunctionCallNode(self.context, tokens) )
            
        else:
            print('Unhandled token type %d' % token.type)
            assert(0)
    
    def __str__(self):
        return '<ContainerNode>'