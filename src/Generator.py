from ContainerNode import ContainerNode
from Tokenizer import Tokenizer
from Token import *

class Generator:
    def __init__(self, string):
        # Resulting string
        self.result = ''
        
        # Code workspace
        self.workspace = {}
        
        # Create a root node
        self.root = ContainerNode(self)
        
        string = self.__processString(string)
        
        tokens = self.__processTokens( Tokenizer.tokenize(string) )
        
#         print('#'*20)
#         for i in tokens:
#             print(i)
      
        # Create the initial children from tokens
        self.root.createChildren( tokens )
        
        # Execute the root node
        self.root.execute()
        
    def __processString(self, string):
        return string
    
    def __processTokens(self, tokens):
        processed = []
        
        prevToken = None
        
        while len(tokens):
            keep = True
            
            token = tokens[0]
            if prevToken and (prevToken.type in [TOKEN_CODE_END, TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_IF, TOKEN_CONDITIONAL_ELSE, TOKEN_CONDITIONAL_ELIF, TOKEN_LOOP_START, TOKEN_LOOP_END]):
                if token.type == TOKEN_TEXT:
                    if token.body == '\n':
                        # Remove the token
                        keep = False
                    elif token.body[0] == '\n':
                        token.body = token.body[1:]
                
            prevToken = token
            tokens.pop(0)
            if keep:
                processed.append(token)

        return processed
        
    def createContainer(self):
        return ContainerNode(self)


    @staticmethod
    def process(string):
        return Generator(string).result