
from Generator import *

from Utils import *

import re

a = re.compile('<% function [a-zA-Z]{1}[a-zA-Z0-9]*\([a-zA-Z0-9 ,]*\) %>')

input = '''\

<% code %>

asdf = 34

<~ code %>

<% function fnc2(arg1) %>
fnc2 arg1 <= arg1 %> GLOBAL ? <= a %>
<~ function %>


<% function fnc1(arg1) %>
<% call fnc2(4) %>
fnc1 arg1 <= arg1 %>
<~ function %>

<% for i in range(5) %>

    <% call fnc1(i) %>

<~ for %>

wet <= i %>

'''
 
out = Generator.convert(input)
 
print( '"%s"' % out )