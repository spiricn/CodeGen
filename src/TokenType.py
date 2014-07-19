import re

class TokenType(object):
    def __init__(self, regex, tokenType, tokenClass):
        self.tokenClass = tokenClass
        self.regex = re.compile(regex)
        self.r = regex
        self.tokenType = tokenType
        
    def matches(self, string):
        return self.regex.match(string) != None
    
    def instantiate(self, body):
        return self.tokenClass(self.tokenType, body)
    
    def __str__(self):
        return '<TokenType type=%d ; regex="%s">' % (self.tokenType, self.regex)