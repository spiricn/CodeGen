import sys



from Generator import Generator


g = Generator()


def code_test():
    
#     input = '''\
# START_BEGIN
#     Segment before the code.
# END_BEGIN
# <% code >
# # START
# a = 3
# b = 4
# for i in range(10):
#     b += i
# c = a+b 
# # END
# <~ code >
# 
# Evaluation block: <= c >
# START_END
#     Segment after the code.
# END_END
# '''
    
    input = '''\
<% code >
a = False
b = True
<~ code >


<% if a >
    a passed!
<% elif b >
    b passed!
<% else >
    none passed :(
<~ if >
'''
    
    gen = Generator()
    
    gen.execute(input)
    
    print('#'*30)
    print( gen.getResult() )
    


code_test();