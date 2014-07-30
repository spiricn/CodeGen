from codegen.ContainerNode import ContainerNode
from codegen.Tokenizer import Tokenizer
from codegen.Token import *
from codegen.TokenType import *
from codegen.WhileLoopToken import WhileLoopToken
from codegen.ConditionalToken import ConditionalToken
from codegen.TextToken import TextToken
from codegen.EvalToken import EvalToken
from codegen.ConditionalToken import ConditionalToken
from codegen.CodeToken import CodeToken
from codegen.IncludeToken import IncludeToken
from codegen.ForLoopToken import ForLoopToken
from codegen.FunctionToken import FunctionToken
from codegen.FileSystemIncludeHandler import FileSystemIncludeHandler
import os
    
class Generator:
    FLAG_OVERWRITE = 1 << 0
    
    def __init__(self):
        # Code workspace
        self.workspace = {}
        
        self.__fileIncludeHandler = FileSystemIncludeHandler()
        
        self.__searchHandlers = [ self.__fileIncludeHandler ]
        
        self.__functions = {}
        
        self.workspace['CONTEXT'] = self
        
        
    def processFile(self, inputFilePath, outputFilePath=None, flags = 0):
        with open(inputFilePath, 'r') as file:
            inputFileString = file.read()
        
        result = self.process(inputFileString)
        
        if outputFilePath:
            if (flags & Generator.FLAG_OVERWRITE == 0) and os.path.exists(outputFilePath):
                raise RuntimeError("File \"%s\" already exists (enable overwriting via FLAG_OVERWRITE)" % outputFilePath)
            
            with open(outputFilePath, 'w') as file: 
                file.write(result)
            
        return result
        
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
        
    def write(self, string):
        self.__result += string
        
    def execute(self, path):
        code = self.__getIncludeContent(path)
        
        if code == None:
            raise RuntimeError('Error getting content from location \"%s\"' % path)
        
        exec(code, self.workspace)
        
    @staticmethod
    def convert(string):
        return Generator().process(string)
    
    def __getIncludeContent(self, file):
        for handler in self.__searchHandlers:
            content = handler.getIncludeContent(file)
            
            if content != None:
                return content

        # None of the handlers         
        return None
    
    def __processString(self, string):
        # We're just using \n instead of \r\n
        string = string.replace('\r\n', '\n')
        
        res = ''
        
        r = re.compile('[^ \t]')
        
        for line in string.split('\n'):
            if line.startswith('\\'):
                match = r.search(line[1:])
                if match:
                    line = line[1:][match.span()[0]:]
                    
            res += '%s\n' % line
            
        # Escaped new lines
        res = res.replace('\\\n', '')
                
        return res[:-1]
    
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
                                                 TOKEN_CONDITIONAL_ELSE, TOKEN_CONDITIONAL_ELIF, TOKEN_FOR_LOOP_START, \
                                                 TOKEN_FOR_LOOP_END, TOKEN_INCLUDE, TOKEN_WHILE_LOOP_START, TOKEN_WHILE_LOOP_END,
                                                 TOKEN_FUNCTION_END, TOKEN_FUNCTION_CALL, TOKEN_FUNCTION_BEGIN
                                                 ]):
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
    
    def addFunction(self, name, node):
        self.__functions[name] = node
    
    def getFunction(self, name):
        if name not in self.__functions:
            raise RuntimeError('Function \"%s\" does not exist' % name)
        
        return self.__functions[name]

    # Types of tokens we're after (order matters!)
    __tokenTypes = [
        # Conditional
        TokenType('^<% if .* %>$', TOKEN_CONDITIONAL_IF, ConditionalToken),
        TokenType('^<% else %>$', TOKEN_CONDITIONAL_ELSE, ConditionalToken),
        TokenType('^<% elif .* %>$', TOKEN_CONDITIONAL_ELIF, ConditionalToken),
        TokenType('^<~ if %>$', TOKEN_CONDITIONAL_END, ConditionalToken),
        
        # Code
        TokenType('^<% code .* %>$', TOKEN_CODE_START, CodeToken),
        TokenType('^<% code %>$', TOKEN_CODE_START, CodeToken),
        TokenType('^<~ code %>$', TOKEN_CODE_END, CodeToken),
        
        # For loop
        TokenType('^<% for .* %>$', TOKEN_FOR_LOOP_START, ForLoopToken),
        TokenType('^<~ for %>$', TOKEN_FOR_LOOP_END, ForLoopToken),
        
        # Eval
        TokenType('^<= .* %>$', TOKEN_EVAL, EvalToken),
        
        # Include
        TokenType('^<% include .* %>$', TOKEN_INCLUDE, IncludeToken),
        
        # While loop
        TokenType('^<% while .* %>$', TOKEN_WHILE_LOOP_START, WhileLoopToken),
        TokenType('^<~ while %>$', TOKEN_WHILE_LOOP_END, WhileLoopToken),
        
        # Functions
        TokenType('<% function [a-zA-Z]{1}[a-zA-Z0-9]*\([a-zA-Z0-9 ,]*\) %>', TOKEN_FUNCTION_BEGIN, FunctionToken),
        TokenType('<~ function %>', TOKEN_FUNCTION_END, FunctionToken),
        TokenType('<% call [a-zA-Z]{1}[a-zA-Z0-9]*\([a-zA-Z0-9 ,]*\) %>', TOKEN_FUNCTION_CALL, FunctionToken),
        
        
        # Text if all else fails
        TokenType('.*', TOKEN_TEXT, TextToken)
    ]
    