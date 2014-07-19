from Generator import *
import unittest

class Nesting(unittest.TestCase):
    def setUp(self):
        pass
     
    def test_basicIf(self):
        '''
        Basic nested if tag test
        '''
        
        input = '''\
<% code >
a = 42
<~ code >
<% if True >
<% if False >
Fail
<% else >
Inner conditional
<~ if >
<% for i in range(2) >
Inner loop
<~ for >
Inner eval <= a >
<~ if >
'''
        expected = 'Inner conditional\nInner loop\nInner loop\nInner eval 42\n'
        
        output = Generator.convert(input)
        
        self.assertEqual( output, expected )
        
    def test_basicFor(self):
        '''
        Basic nested for tag test.
        '''
        
        input = '''\
<% for i in range(2) >
<% if i == 0 >
First iteration if
<% elif i == 1 >
Second iteration if
<~ if >
i=<= i >
<% for j in range(2) >
Inner loop j=<= j >
<~ for >
<~ for >
'''
        expected = "First iteration if\ni=0\nInner loop j=0\nInner loop j=1\nSecond iteration if\ni=1\nInner loop j=0\nInner loop j=1\n"
        
        output = Generator.convert(input)
        
        self.assertEqual( output, expected )

if __name__ == '__main__':
    unittest.main()
