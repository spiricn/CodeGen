from Node import *
from TextNode import TextNode
from CodeNode import CodeNode
from ConditionalNode import ConditionalNode
from EvalNode import EvalNode
from LoopNode import LoopNode 
from Token import *

class ContainerNode(Node):
    def __init__(self, context):
        Node.__init__(self, context, NODE_CONTAINER)
        
        self.children = []
        
            
    def execute(self):
        for child in self.children:
            child.execute()
            
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
            
        elif token.type == TOKEN_LOOP_START:
            self.children.append( LoopNode(self.context, tokens) )
        else:
            assert(0)
    
    def __str__(self):
        return '<ContainerNode>'