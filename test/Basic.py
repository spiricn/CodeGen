from codegen.Generator import *
from codegen.Utils import *
import unittest

class Basic(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        inputString = '\nFirst line.\nSecond line\nThird line.\n'
        
        output = Generator.convert(inputString)
        
        # Input should be the same as output
        self.assertEqual( inputString, output )
        
    def test_code(self):
        '''
        Simple code tags test.
        '''
        
        inputString = '''\
First line.
<% code %>
a = 2
b = 3
c = a+b
<~ code %>
Second line.
<% code %>
d = a+b+c
<~ code %>
'''
        expected = 'First line.\nSecond line.\n'
        
        output = Generator.convert(inputString)
        
        self.assertEqual( output, expected )
        
    def test_eval(self):
        '''
        Simple evaluation tag test.
        '''
        
        inputString = '''\
First line.
<% code %>
a = 3; b = 4; c = a+b;
<~ code %>
Value of c is <= c %>
'''
        
        expected = 'First line.\nValue of c is 7\n'
        
        output = Generator.convert(inputString)
        
        self.assertEqual( output, expected )
        
        
    def test_basicConditional(self):
        '''
        Simple conditional tag test.
        '''
        
        inputString = '''\
<% if True and 1 == 1 %>
Pass
<~ if %>
'''
        expected = 'Pass\n'
        
        output = Generator.convert(inputString)
        
        self.assertEqual( output, expected )        
    
    def test_multiConditional(self):
        '''
        Multi conditional tag test.
        '''
        
        inputString ='''\
<% if True and 0 %>
<~ if %>
<% if True or 3 == 4 %>
Pass if<~ if %>
<% if False and True %>
Pass if
<~ if %>
<% if False and 3 == 3 %>
Fail
<% elif True or False %>
Pass elif<~ if %>
<% if False and True %>
Fail
<% elif False and True %>
Fail
<% else %>
Pass else
<~ if %>
'''
        output = Generator.convert(inputString)
        
        expected = 'Pass ifPass elifPass else\n'
        
        self.assertEqual( output, expected )
        
    def test_basicloop(self):
        '''
        Basic loop test.
        '''
        
        inputString = '''\
<% for i in range(3) %>
a
<~ for %>
'''
        expected ='''\
a
a
a
'''
        output = Generator.convert(inputString)
        
        self.assertEqual(output, expected)
        
    def test_multiLoop(self):
        '''
        Multi loop test.
        '''
        
        inputString = '''\
<% for i in range(50) %>
<~ for %>
<% for i in range(2) %>
a<~ for %>
<% for i in range(3) %>
b
<~ for %>
'''
        output = Generator.convert(inputString)
        
        expected = 'aab\nb\nb\n'
        
        self.assertEqual(output, expected)
        
    def test_whileLoop(self):
        '''
        While loop test.
        '''
        
        input = "<% code %>a = 3<~ code %><% while a %>a is <= a %><% code %>a -= 1<~ code %><~ while %>"
        
        output = Generator.convert(input)
        
        expected = 'a is 3a is 2a is 1'

        self.assertEqual(output, expected)
        
    def test_inlineCode(self):
        '''
        Inline code test.
        '''
        
        input = '<% code a=3 %>Value of a is <= a %>'
        
        output = Generator.convert(input)
        
        expected = 'Value of a is 3'

        self.assertEqual(output, expected)
        
    def test_basicFunction(self):
        '''
        Basic function call test.
        '''

        input = '''\
<% function test(arg1, arg2) %>
Function result: arg1=<= arg1 %> , arg2=<= arg2 %><~ function %>
<% call test(2, 3) %>'''
        
        output = Generator.convert(input)
        
        expected = 'Function result: arg1=2 , arg2=3'
        
        self.assertEqual(output, expected)
        
    def test_newLineEscaping(self):
        '''
        New line escaping test.
        '''
        
        input = '''\
first\\
second\\
third\\
'''

        output = Generator.convert(input)
        
        expected = 'firstsecondthird'
        
        self.assertEqual(output, expected);
        
    def test_whiteSpaceEscaping(self):
        '''
        White space escaping test.
        '''
        
        input = '''\
\\    \tfirst\\
\\    second\\
\\  third\\
'''
        
        output = Generator.convert(input)
        
        expected = 'firstsecondthird'
        
        self.assertEqual(output, expected);
        
if __name__ == '__main__':
    unittest.main()
