from Token import *

class Tokenizer:
    def __init__(self, string, tokenTypes):
        self.string = string
        self.tokenTypes = tokenTypes
        
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
    def tokenize(string, tokenTypes):
        '''
        Tokenizes an entire string.
        @return: List of all tokens the string contains
        '''
        return Tokenizer(string, tokenTypes).getAll()
    
    def getAll(self):
        tokens = []
        
        while True:
            token = self.next()
            
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

            for entry in self.tokenTypes:
                if entry.matches(body):
                    token = entry.instantiate(body)
                    break
                
            if token == None:
                print('Token not matched')
            
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
        
        while idx < stringLen -1 :
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
