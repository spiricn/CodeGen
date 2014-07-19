from Generator import *
import unittest
import os

INCLUDE_DIR_PATH = './include_dir/dir1/dir2'

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
        
if __name__ == '__main__':
    unittest.main()
