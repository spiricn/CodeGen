
from Generator import *

from Utils import *

import re

a = re.compile('<% function [a-zA-Z]{1}[a-zA-Z0-9]*\([a-zA-Z0-9 ,]*\) %>')

input = '''\
<% function test(arg1, arg2) %>
FUNCTION_START
    arg1 is <= arg1 %> 
    arg2 is <= arg2 %> 
FUNCTION_END
<~ function %>

<% for i in range(5) %>
<% call test(i, i) %>
<~ for %>

'''

out = Generator.convert(input)

print( '"%s"' % out )
