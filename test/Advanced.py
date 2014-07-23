from Generator import *
import unittest
import os

RESOURCE_DIR = './rsrc'

INCLUDE_DIR_PATH = os.path.join(RESOURCE_DIR, 'include_dir')

TMP_DIR = os.path.join( RESOURCE_DIR, 'tmp' )

class IncludeHandler:
    '''
    Class used for custom include handler tests
    '''
    
    def __init__(self, directory):
        self.__directory = directory
    
    def getIncludeContent(self, file):
        path = os.path.join(self.__directory, file)
         
        file = open(path, 'r')
         
        content = file.read()
         
        file.close()
         
        return content
     
class Advanced(unittest.TestCase):
    def setUp(self):
        pass

    def test_basicInclude(self):
        '''
        Basic file including from a directory test.
        '''
        
        inputString = '<% include include_file1.py %>\n<% include include_file2.py %>\n'
        
        generator = Generator()
        
        generator.addSearchPath( INCLUDE_DIR_PATH )
        
        output = generator.process(inputString)
        
        expected = 'include1 content\ninclude2 content\n'

        # Input should be the same as output
        self.assertEqual( output, expected)
        
    def test_recursiveInclude(self):
        '''
        Recursive file including from a directory.
        '''
        
        inputString = '<% include include_recursive.py %>'
    
        generator = Generator()
        
        generator.addSearchPath( INCLUDE_DIR_PATH )
        
        output = generator.process(inputString)
        
        expected = 'include recursive\ninclude1 content\n'

        # Input should be the same as output
        self.assertEqual( output, expected)
        
    def test_includeHandler(self):
        '''
        Custom include handler test.
        '''
        
        inputString = '<% include include_file1.py %>'
    
        generator = Generator()
        
        generator.addSearchHandler( IncludeHandler(INCLUDE_DIR_PATH) )
        
        output = generator.process(inputString)
        
        expected = 'include1 content'

        # Input should be the same as output
        self.assertEqual( output, expected)
        
    def test_advancedLoops(self):
        '''
        Multi variable for loop test.
        '''
        
        input='''\
<% code %>
array = ['a', 'b', 'c']
<~ code %>
<% for c,i in enumerate(array) %>
array[<= c %>] = <= i %><~ for %>
'''

        output = Generator.convert(input)
                
        expected = 'array[0] = aarray[1] = barray[2] = c'
        
        self.assertEqual( output, expected )
        
    def test_fileToMemoryProcess(self):
        '''
        Basic file to memory processing test.
        '''
        g = Generator()
        
        res = g.processFile( os.path.join(RESOURCE_DIR, 'test_template_1.py') )
        
        expected = 'Value of a is 42'
        
        self.assertEqual(res, expected)
        
    def test_fileToFileProcess(self):
        '''
        Basic file to file processing.
        '''
        g = Generator()
        
        outPath = os.path.join(TMP_DIR, "out_test_tmp1.py")
        
        # Delete the file if it exists
        if os.path.exists(outPath):
            os.remove(outPath)
        
        g.processFile( os.path.join(RESOURCE_DIR, 'test_template_1.py'), outPath)
        
        # Read the contents of the created file
        with open(outPath, 'r') as file:
            result = file.read() 
        
        expected = 'Value of a is 42'
        
        self.assertEqual(result, expected)
        
        # Cleanup
        if os.path.exists(outPath):
            os.remove(outPath)
        
    def test_fileToFileOverwrite(self):
        '''
        Basic file to file processing (with overwrite).
        '''
        
        outPath = os.path.join(TMP_DIR, "out_test_tmp1.py")
        
        # Create a temporary file
        file = open(outPath, 'w')

        file.close()        
        
        self.assertTrue( os.path.exists(outPath) )
         
        generator = Generator()
        
        inPath = os.path.join(RESOURCE_DIR, 'test_template_1.py')
        
        
        # Try to convert a file without setting the flag (expected to fail)
        try:
            generator.processFile(inPath, outPath, 0)
            self.fail("File overwritten without specifying the overwrite flag")
        except Exception:
            pass
        
        # Try to convert a file with the flag (should pass)
        try:
            generator.processFile(inPath, outPath,  Generator.FLAG_OVERWRITE )
        except Exception:
            self.fail("File not overrwriten after specifying overwrite flag")
        
        # Read the contents of the created file
        with open(outPath, 'r') as file:
            result = file.read() 
         
        expected = 'Value of a is 42'
         
        self.assertEqual(result, expected)
        
        # Cleanup
        if os.path.exists(outPath):
            os.remove(outPath)
            
if __name__ == '__main__':
    unittest.main()
