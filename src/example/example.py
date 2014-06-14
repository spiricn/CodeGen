className = CG_getArg(0)

headerGuard = 'WT_%s_H' % className.upper()


class Test:
    def __init__(self):
	    self.attr = 5
		
		
gTest = Test()
###############################################################################

headerFileName =  '%s.h' % className

CG_convertFile('./example/header.py', headerFileName)

###############################################################################

cppFileName = '%s.cpp' % className


CG_convertFile('./example/source.py', cppFileName)

###############################################################################