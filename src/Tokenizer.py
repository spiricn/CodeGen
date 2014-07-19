from Token import *

class Tokenizer:
    def __init__(self, string):
        self.string = string
        
    def next(self):
        '''
        Processes the string, returning the next token.
        @return: Processed token. May be None in which case the string has been depleted
        '''
        
        tokens = self.__tokenize(1)
        
        return tokens[0] if len(tokens) else None
        
    @staticmethod
    def reconstruct(tokens):
        '''
        Reconstructs a string using a list of tokens
        @param tokens: A list of tokens generated from a string
        @return: Reconstructed string 
        '''
        
        res = ''
        
        for token in tokens:
            res += token.body
            
        return res
    
    @staticmethod
    def tokenize(string):
        '''
        Tokenizes an entire string.
        @return: List of all tokens the string contains
        '''
        tokenizer = Tokenizer(string)
        
        tokens = []
        
        while True:
            token = tokenizer.next()
            
            if token:
                tokens.append(token)
            else:
                break
            
        return tokens
            
    def __tokenize(self, numTokens):
        '''
        Turns a portion of the string into tokens
        @param numTokens: Maximum number of tokens to be created
        @return: A list containing the token objects (minimum length 0, maximum length "numTokens")
        '''
        tokens = []
        
        while numTokens and len(self.string):
            cmd = self.__matchCommand(self.string, 0)
            
            token = None
            
            if cmd == None:
                # String is just text
                body = self.string
            elif cmd[0] == 0:
                # Command at the beggining
                body = self.string[:cmd[1]]
            else:
                # Text at the beggining
                body = self.string[:cmd[0]]
            
            typeMap = {
                # Conditional
                TOKEN_CONDITIONAL_IF : ConditionalToken,
                TOKEN_CONDITIONAL_ELSE : ConditionalToken,
                TOKEN_CONDITIONAL_ELIF : ConditionalToken,
                TOKEN_CONDITIONAL_END : ConditionalToken,
                
                # Text
                TOKEN_TEXT : ConditionalToken,
                
                # Code
                TOKEN_CODE_START : CodeToken,
                TOKEN_CODE_END: CodeToken,
                
                # Loop
                TOKEN_LOOP_START : LoopToken,
                TOKEN_LOOP_END : LoopToken,
                
                # Eval
                TOKEN_EVAL : EvalToken
            }
            
            type = self.__getTokenType(body)
            
            token = typeMap[type](type, body)
            
            tokens.append( token )
            
            self.string = self.string[len(token.body):]
            
            numTokens -= 1
            
        return tokens
        
    def __matchCommand(self, string, start):
        '''
        Matches a single command block (for instance "<% code >", "<= expression >", "<~ code >", etc..
        
        @param string: A string to be parsed
        @param start: Starting index used for parsing
        
        @return: Returns index pair of the matched command e.g. [startIndex, endIndex] or None if command has not been found
        '''
        
        idx = start
        
        stringLen = len(string)
        
        start = -1
        
        end = -1
        
        while idx < stringLen:
            if string[idx] == '<' and ( (string[idx+1] == '%' or string[idx+1] == '=') or string[idx+1] == '~' ):
                start = idx
                
                
                
            elif string[idx] == '>' and string[idx+1] == '\n':
                end = idx+1
                break
                
            idx += 1
                
        if start == -1 or end == -1:
            return None
        else:
            return [start, end]
        
    @staticmethod
    def __getTokenType(body):
        # Code
        if body == '<% code >':
            return TOKEN_CODE_START
        
        elif body == '<~ code >':
            return TOKEN_CODE_END
        
        # Evaluation
        elif body.startswith('<= ') and body.endswith(' >'):
            return TOKEN_EVAL
        
        # Conditional
        elif body.startswith('<% if ') and body.endswith(' >'):
            return TOKEN_CONDITIONAL_IF
        
        elif body.startswith('<% elif ') and body.endswith(' >'):
            return TOKEN_CONDITIONAL_ELIF
        
        elif body == '<% else >':
            return TOKEN_CONDITIONAL_ELSE
        
        elif body == '<~ if >':
            return TOKEN_CONDITIONAL_END
        
        # Loop
        elif body.startswith('<% for ') and body.endswith(' >'):
            return TOKEN_LOOP_START
        
        elif body == '<~ for >':
            return TOKEN_LOOP_END
        
        else:
            return TOKEN_TEXT
