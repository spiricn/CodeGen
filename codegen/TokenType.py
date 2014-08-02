import re

class TokenType(object):
    def __init__(self, regex, tokenType, tokenClass):
        self.tokenClass = tokenClass
        self.regex = re.compile(regex)
        self.r = regex
        self.tokenType = tokenType
        
    def matches(self, string):
        return self.regex.match(string) != None
    
    def instantiate(self, body, template, sourceLocation):
        return self.tokenClass(self.tokenType, body, template, sourceLocation)
    
    def __str__(self):
        return '<TokenType type=%d ; regex="%s">' % (self.tokenType, self.regex)