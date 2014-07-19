from ContainerNode import ContainerNode
from Tokenizer import Tokenizer
from Token import *
from TokenType import *
import os

class FileSystemIncludeHandler:
    def __init__(self):
        self.__locations = []
        
    def addSearchPath(self, location):
        self.__locations.append( location )
        
    def getIncludeContent(self, file):
        for location in self.__locations:
            for directory, dirNames, fileNames in os.walk(location):
                for i in fileNames:
                    if i == file:
                        file = open(os.path.join(directory, i), 'r')
                        
                        content = file.read()
                        
                        file.close()
                        
                        return content

        return None
    
class Generator:
    def __init__(self):
        # Code workspace
        self.workspace = {}
        
        self.__fileIncludeHandler = FileSystemIncludeHandler()
        
        self.__searchHandlers = [ self.__fileIncludeHandler ]
        
    def process(self, string):
        # Resulting string
        self.__result = ''
        
        # Create a root node
        rootNode = ContainerNode(self)
        
        string = self.__processString(string)
        
        self.tokenizer = Tokenizer(string, Generator.__tokenTypes)
        
        tokens = self.tokenizer.getAll()
        
        tokens = self.__processIncludes( tokens )
        
        tokens = self.__processTokens( tokens )
        
        # Create the initial children from tokens
        rootNode.createChildren( tokens )
        
        # Execute the root node
        rootNode.execute()
        
        return self.__result
    
    def addSearchPath(self, path):
        self.__fileIncludeHandler.addSearchPath( path )
        
    def addSearchHandler(self, handler):
        self.__searchHandlers.append( handler )
        
    def __getIncludeContent(self, file):
        for handler in self.__searchHandlers:
            content = handler.getIncludeContent(file)
            
            if content != None:
                return content

        # None of the handlers         
        return None
    
    def write(self, string):
        self.__result += string
        
    def __processString(self, string):
        # TODO string preprocessing, such as convertin \r\n to \n etc.
        return string
    
    def __processTokens(self, tokens):
        '''
        A generic processing pass. Does things like removing \n after various blocks
        
        @param tokens: Tokens to preform the pass on.
        
        @return: Processed token list
        '''
        processed = []
        
        prevToken = None
        
        while len(tokens):
            keep = True
            
            token = tokens[0]
            if prevToken and (prevToken.type in [TOKEN_CODE_END, TOKEN_CONDITIONAL_END, TOKEN_CONDITIONAL_IF, \
                                                 TOKEN_CONDITIONAL_ELSE, TOKEN_CONDITIONAL_ELIF, TOKEN_LOOP_START, \
                                                 TOKEN_LOOP_END, TOKEN_INCLUDE]):
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

    def __processIncludes(self, tokens):
        '''
        Preforms a recursive "include" pass on given list of tokens
        
        @param tokens: Tokens to preform the pass on.
        
        @return: Processed token list
        '''
        
        processed = []
        
        for token in tokens:
            if token.type == TOKEN_INCLUDE:
                content = self.__getIncludeContent( token.file )
                
                if content == None:
                    raise RuntimeError('Include "%s" not found' % token.file)
                    
                    continue
                
                self.tokenizer.string = content
                
                included = self.tokenizer.getAll() 
                
                # Process for more includes
                included = self.__processIncludes( included )
                
                for i in included:
                    processed.append( i )
                    
            else:
                processed.append(token)
        
        return processed
        
    def createContainer(self):
        return ContainerNode(self)

    @staticmethod
    def convert(string):
        return Generator().process(string)
    
    # Types of tokens we're after (order matters!)
    __tokenTypes = [
        # Conditional
        TokenType('^<% if .* %>$', TOKEN_CONDITIONAL_IF, ConditionalToken),
        TokenType('^<% else %>$', TOKEN_CONDITIONAL_ELSE, ConditionalToken),
        TokenType('^<% elif .* %>$', TOKEN_CONDITIONAL_ELIF, ConditionalToken),
        TokenType('^<~ if %>$', TOKEN_CONDITIONAL_END, ConditionalToken),
        
        # Code
        TokenType('^<% code %>$', TOKEN_CODE_START, CodeToken),
        TokenType('^<~ code %>$', TOKEN_CODE_END, CodeToken),
        
        # Loop
        TokenType('^<% for .* %>$', TOKEN_LOOP_START, LoopToken),
        TokenType('^<~ for %>$', TOKEN_LOOP_END, LoopToken),
        
        # Eval
        TokenType('^<= .* %>$', TOKEN_EVAL, EvalToken),
        
        # Include
        TokenType('^<% include .* %>$', TOKEN_INCLUDE, IncludeToken),
        
        # Text if all else fails
        TokenType('.*', TOKEN_TEXT, TextToken)
    ]
    