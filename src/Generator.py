import traceback
import sys

from Utils import * 

'''
-------------------------------------------------------------------------------

Code block:

    <% code >
    
        # Code
    
    <~ code >

-------------------------------------------------------------------------------
    
Evaluation block:
    <= variable >
    
-------------------------------------------------------------------------------
    
Conditional:
    <% if 'conditional_expression' >
    
        # Code
    
    <% elif 'another_expression' >
    
        # Code
    
    <~ if >

-------------------------------------------------------------------------------

For loop:
    <% for 'values' in 'container' >
    
        # Code
    
    <~ for >
    
-------------------------------------------------------------------------------
'''

kSTART_EVAL = '<%= '

kSTART_CODE = '<% '

kSTART_LOOP = '<%for '

kSTART_IF = '<%if '


BLOCK_INVALID = -1
BLOCK_CODE = 0
BLOCK_EVAL = 1
BLOCK_CONDITIONAL = 2

def commandBody(start, end, string):
    return string[start[1]:end[0]]
    
class CodeBlock:
    def __init__(self, start, end, string):
        self.blockStart = start
        self.blockEnd = end
        self.body = commandBody(start, end, string)
        self.type = BLOCK_CODE
        
    def getRange(self):
        return [self.blockStart[0], self.blockEnd[1]]
        
    def __str__(self):
        return '<CodeBlock start=%s end=%s>' % (str(self.blockStart), str(self.blockEnd))
    
    
class EvalBlock:
    def __init__(self, start, string):
        self.blockStart = start
        self.body = string[self.blockStart[0] : self.blockStart[1]][3:-2]
        self.type = BLOCK_EVAL
        
    def getRange(self):
        return self.blockStart
        
    def __str__(self):
        return '<EvalBlock block=%s>' % str(self.blockStart)
    

CONDITION_IF = 0
CONDITION_ELIF = 1
CONDITION_ELSE = 2
CONDITION_FI = 3
   
class Condition:
    def __init__(self, query, body, type):
        self.query = query
        self.body = body
        self.type = type
        
    def __str__(self):
        return '<Condition type=%s>' % self.type
        
class ConditionalBlock:
    def __init__(self, conditions, string):
        self.conditions = []
        self.type = BLOCK_CONDITIONAL
        
        for c,condition in enumerate(conditions):
            query = slice(string, condition)
            type = 0
            if query.startswith('<% if '):
                type = CONDITION_IF
            elif query.startswith('<% elif '):
                type = CONDITION_ELIF
            elif query.startswith('<% else '):
                type = CONDITION_ELSE
            elif query.startswith('<~ if >'):
                type = CONDITION_FI
            else:
                # TODO error
                pass
                
            # Extract the query string
            query = query[len(query[3:].split(' ')[0])+4:-2]
            
            if type != CONDITION_FI:
                # Get the body
                body = slice(string, [condition[1], conditions[c+1][0]])
                
                self.conditions.append( Condition(query, body, type) )
            else:
                self.conditions.append( Condition(None, None, type) )
                
        self.range = [conditions[0][0], conditions[-1][1]]
         
    def getRange(self):
        return self.range
        
class Generator:
    def __init__(self):
        self.workspace = {}
        self.result = ''
    
    def getResult(self):
        return self.result
    
    def _doEvalBlock(self, code):
        try:
            self.result += str( eval(code, self.workspace) )
        except Exception as e:
            print('Error evaluating expression "%s"; reason: %s' % (code, e))
            traceback.print_exc(file=sys.stdout)
            raise
    
    def _doCodeBlock(self, code):
        try:
            exec(code, self.workspace)
        except Exception as e:
            print('Error executing expression "%s"; reason %s' % (code, e))
            traceback.print_exc(file=sys.stdout)
            raise
        
    def _doLoopBlock(self, code):
        loop = code.split(':\n')[0]
        
        vars = loop.split('in')[0].replace(' ', '')
        varList= vars.split(',')
        
        container = loop.split('in')[1].replace(' ', '')
        
        body = code.split(':\n')[1]
    
        tmp = {
            'self' : self,
            'body' : body
        }    
        
        e = '''\
for %s in %s:

''' % (vars, container)

        for var in varList:
            e += '''\
    self.workspace['%s'] = %s
''' % (var, var)


    
        e += '''\
    self.execute(body)
'''
        try:
            exec(e, tmp)
        except Exception as e:
            print('Error executing loop; reason %s' % e)
        
    
    def _matchEnd(self, code, start):
        numOpenBrackets = 0
        
        for i in range(len(code[start:])):
            if code[start+i] == '<' and code[start+i+1] == '%':
               numOpenBrackets += 1
            elif code[start+i] == '%' and code[start+i+1] == '>':
                if numOpenBrackets > 0:
                    numOpenBrackets -= 1
                else:
                    return start+i+1
        return -1
    
    
    
    
    def _doIfBlock(self, code):
        condition = code.split('\n')[0]
        body = code[len(condition):]
         
        if eval(condition, self.workspace):
            # Condition passed
            self.execute(body)
        else:
            print('condigion failed')
         
         
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
    
    def __getCommandType(self, block):
        if block == '<% code >':
            return BLOCK_CODE
        elif block.startswith('<= '):
            return BLOCK_EVAL
        elif block.startswith('<% if '):
            return BLOCK_CONDITIONAL
        else:
            return BLOCK_INVALID
        
    def __getCodeCommand(self, string, start):
        end = self.__matchCommand(string, start[1])
        
        if end == None:
            print('Unmatched code block (missing <~ code >)')
            return None
        elif string[end[0]:end[1]] != '<~ code >':
            print('Blocks within code blocks not allowed')
            return None
        
        return CodeBlock(start, end, string)
    
    def __getEvalCommand(self, string, start):
        return EvalBlock(start, string)
    
    def __getConditionalCommand(self, string, start):
        conditions = []
        
        conditions.append(start)
        
        
        prevIndices = start
        
        while True:
            cmd = self.__matchCommand(string, prevIndices[1])
            
            commandStr = slice(string, cmd)
            
            prevIndices = cmd
            
            conditions.append(cmd)
            
            if commandStr == '<~ if >':
                # Found the end
                break
                
        return ConditionalBlock(conditions, string)
    
    def getCommand(self, string, start):
        # Find the first command in the string
        startCommand = self.__matchCommand(string, start)
        
        if startCommand == None:
            # No commands found
            return None
        
        # Openning command block
        commandStart = string[startCommand[0]:startCommand[1]]
        
        commandType = self.__getCommandType(commandStart)
        
        if commandType == BLOCK_CODE:
            return self.__getCodeCommand(string, startCommand)
        elif commandType == BLOCK_EVAL:
            return self.__getEvalCommand(string, startCommand)
        elif commandType == BLOCK_CONDITIONAL:
            return self.__getConditionalCommand(string, startCommand)
        else:
            return None
        
    def __doConditionalCommand(self, cmd):
        passed = None
        
        for condition in cmd.conditions:
            if condition.type == CONDITION_FI:
                print('a')
                # None of the conditions passed
                break
            elif condition.type == CONDITION_ELSE:
                # Reached else..
                passed = condition
                break
            # Evaluate a condition
            elif eval(condition.query, self.workspace):
                # Condition passed
                passed = condition
                break
            
        if passed == None:
            # Do nothing
            return
        
        # Execute body
        self.execute(condition.body)
    
    def execute(self, string):
        while len(string):
            # First command
            cmd = self.getCommand(string, 0)
            
            print(cmd)
            
            if cmd == None:
                # No commands left in the string
                self.result += string
                break
            else:
                cmdRange = cmd.getRange()
                
                # Plain text before first command
                self.result += string[:cmdRange[0]]
                
                if cmd.type == BLOCK_CODE:
                    self._doCodeBlock(cmd.body)
                elif cmd.type == BLOCK_EVAL:
                    self._doEvalBlock(cmd.body)
                elif cmd.type == BLOCK_CONDITIONAL:
                    self.__doConditionalCommand(cmd)
                else:
                    print('Unhandled command type %d' % cmd.type)
        
        
                string = string[cmdRange[1]:]
