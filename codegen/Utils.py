def slice(string, indices):
    '''
    Slices a string using the given indices
    
    @param string: String to be sliced.
    @param indices: Indices tuple (e.g. [startIndex, endIndex]).
    @return: Sliced string.
    '''
    
    return string[indices[0]:indices[1]]


def dprint(string):
    print('"%s"' % string)
    
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)