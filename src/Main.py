
from Generator import *

from Utils import *

import re



a = re.compile('<% function [a-zA-Z]{1}[a-zA-Z0-9]*\([a-zA-Z0-9 ,]*\) %>')



input = '''\

<% function test(arg1, arg2) %>

    arg1 is <= arg1 %>
    arg2 is <= arg2 %>
    
<~ function %>


<% call test(i, i) %>

'''

out = Generator.convert(input)

print( '"%s"' % out )
