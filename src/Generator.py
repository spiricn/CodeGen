import traceback
import sys

class Generator:
    def __init__(self):
        self.workspace = {}
        self.result = ''
    
    def getResult(self):
        return self.result
    
    def doEvalBlock(self, code):
        try:
            return str( eval(code, self.workspace) )
        except Exception as e:
            print('Error evaluating expression "%s"; reason: %s' % (code, e))
            traceback.print_exc(file=sys.stdout)
            raise
    
    def doCodeBlock(self, code):
        try:
            exec(code, self.workspace)
        except Exception as e:
            print('Error executing expression "%s"; reason %s' % (code, e))
            traceback.print_exc(file=sys.stdout)
            raise
    
    def matchEnd(self, code, start):
        for i in range(len(code[start:])):
            if code[start+i] == '%' and code[start+i+1] == '>':
                return start+i+1
        return -1
    
    def write(self, string):
        self.result += string
        
    def doCode(self, code):
        self.result = ''
        
        numErrors = 0    
        currIdx = 0
        
        # Iterate over entire template
        while currIdx < len(code):
            # Find opening bracket (i.e. "<%")
            if code[currIdx] == '<' and code[currIdx+1] == '%':
                if code[currIdx+2] == '=' and code[currIdx+3] == ' ':
                    # It's an evaluation block
                    parseFnc = self.doEvalBlock
                    start = currIdx + 4
                else:
                    # It's a code block
                    start = currIdx + 3
                    parseFnc = self.doCodeBlock;
                
                # Match the previously opened bracket
                end = self.matchEnd(code, start)
                    
                # No matching bracket found
                if end == -1:
                    raise Exception('Unmatched bracket found, aborting')
    
                # Process either expression evaluation or execution
                res = None
                try:
                    res = parseFnc( code[start:end-2] )
                except:
                    numErrors += 1
                    
                if res:
                    self.result += res
    
                # Skip over the processed code
                currIdx = end+1
                    
            else:
                # Plain text, just append it to the result and continiue with parsing
                self.result += code[currIdx]
                currIdx += 1
                
    def doFile(self, path):
        self.result = ''
        code = open(path, 'r').read()
        
        return self.doCode(code)