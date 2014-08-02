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

class Processor(object):
    def __init__(self):
        self.__fileIncludeHandler = FileSystemIncludeHandler()
        
        self.__searchHandlers = [ self.__fileIncludeHandler ]
    
    def addSearchPath(self, path):
        self.__fileIncludeHandler.addSearchPath( path )
        
    def addSearchHandler(self, handler):
        self.__searchHandlers.append( handler )
        
    def getSourceTokens(self, source):
        # String based preprocessing pass
        source = self.__preprocessSourceString(source)
        
        # Tokenize string
        tokens = Tokenizer.tokenize(source, Processor.__tokenTypes)
        
        # Token based preprocessing pass 
        tokens = self.__preprocessTokens( tokens )
        
        return tokens
        
    ###########################################################################
    
    def __preprocessSourceString(self, string):
        '''
        String based pre-processing. Does things such as
        \r\n replacment and newline/white space escaping
        '''
    
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
    
    def __preprocessTokens(self, tokens):
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
                                                 TOKEN_FOR_LOOP_END, TOKEN_WHILE_LOOP_START, TOKEN_WHILE_LOOP_END,
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

        return self.__preprocessTokenIncludes( processed )
    
    def __preprocessTokenIncludes(self, tokens):
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
                
                included = self.getSourceTokens(content)
                
                for i in included:
                    processed.append( i )
                    
            else:
                processed.append(token)
        
        return processed
    
    def __getIncludeContent(self, file):
        for handler in self.__searchHandlers:
            content = handler.getIncludeContent(file)
            
            if content != None:
                return content

        # None of the handlers         
        return None
    
    def __str__(self):
        return '<Processor>'
    
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
    