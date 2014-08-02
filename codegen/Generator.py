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
from codegen.Processor import Processor
import os
    
class Generator:
    '''
    Flags used by the 'processFile' method
    '''
    FLAG_OVERWRITE = 1 << 0
    
    def __init__(self):
        # Code workspace
        self.workspace = {}
        
        # Functtion name->node map
        self.__functions = {}
        
        # Global workspace of the generator
        self.workspace['CONTEXT'] = self
        
        # Processor used to covnert source to tokens
        self.__processor = Processor()
        
    ###########################################################################
    # Public API
    ###########################################################################
        
    def processFile(self, inputFilePath, outputFilePath=None, flags = 0):
        '''
        Processes an input file and returns the processes string (and if needed stores the result in another file)
        
        @param inputFilePath: File containing the input source code.
        @param outputFilePath: Optional parameter; if provided the resulting string is stored in this location.
        @param flags: Optional parameter; File writing flags.
        
        @return: Resulting processed string.
        '''
         
        with open(inputFilePath, 'r') as file:
            inputFileString = file.read()
        
        result = self.process(inputFileString)
        
        if outputFilePath:
            if (flags & Generator.FLAG_OVERWRITE == 0) and os.path.exists(outputFilePath):
                raise RuntimeError("File \"%s\" already exists (enable overwriting via FLAG_OVERWRITE)" % outputFilePath)
            
            with open(outputFilePath, 'w') as file: 
                file.write(result)
            
        return result
        
    def addSearchPath(self, path):
        '''
        Adds a search location on the local drive. This location is searched for file content
        in <% include %> commands and 'execute' method calls
        
        @param path: Directory location.
        '''
        
        if not os.path.exists(path) or not os.path.isdir(path):
            raise RuntimeError('Invalid directory path \"%s\"' % path)
        
        self.__processor.addSearchPath( path )
        
    def addSearchHandler(self, handler):
        '''
        Custom user content include handler.
        
        @param handler: Include handler object
        '''
        
        self.__processor.addSearchHandler( handler )
        
    def process(self, string):
        '''
        Process a string in the context of this generator.
        
        @param string: A string to be processed.
        
        @return: Processed string.
        '''
         
        # Resulting string
        self.__result = ''
        
        # Create a root node
        rootNode = ContainerNode(self)

        template = self.__processor.getSourceTemplate(string)
        
        # Create the initial children from tokens
        rootNode.createChildren( template.tokens )
        
        # Execute the root node
        rootNode.execute()
        
        return self.__result
    
    @staticmethod
    def convert(string):
        '''
        Processes an input string.
        
        @param string: Input string.
        
        @return: Processed input string.
        '''
         
        return Generator().process(string)
    
    ###########################################################################
    # API meant to be used from inside the code
    ########################################################################### 
        
    def write(self, string):
        '''
        Write a string to the result buffer. Inteded to be used from within source code.
        
        @param string: String to be written.
        '''
        
        self.__result += string
        
    def execute(self, path):
        '''
        Execute a file in the generator's workspace.
        
        @param path: File name containing the source code.
        '''
        
        code = self.__getIncludeContent(path)
        
        if code == None:
            raise RuntimeError('Error getting content from location \"%s\"' % path)
        
        exec(code, self.workspace)
        
    ###########################################################################
    # Internal API used by  Code Nodes
    ###########################################################################
        
    def createContainer(self):
        return ContainerNode(self)
    
    def addFunction(self, name, node):
        self.__functions[name] = node
    
    def getFunction(self, name):
        if name not in self.__functions:
            raise RuntimeError('Function \"%s\" does not exist' % name)
        
        return self.__functions[name]

    ###########################################################################
   
    