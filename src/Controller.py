from Generator import Generator

'''

API expoed by the controller (usable by template files):

# Processes a given template source string and stores the result in a file.
#    @param source Template soruce string.
#    @param destFilePath Processed destination file path.
CG_convertSource(source, destFilePath)

# Processes a given template file and stores the result in another file.
#    @param sourceFilePath Source template file path.
#    @param destFilePath Processed destination file path.
CG_convertFile(sourceFilePath, destFilePath)


# Gets the string argument at the given index.
#    @param index Argument index
CG_getArg(index)

# Gets the number of arguments provided for the generator.
CG_getNumArgs

# Write a string to the result buffer without processing
#    @param string String to be written
CG_write(string)

'''
# 
# class Controller:
#     def __init__(self):
#         self.args = []
#         self.generator = Generator()
#     
#     def getArg(self, num):
#         args = self.args[2:]
#         return args[num]
#         
#     def convertFile(self, inputPath, outputPath):
#         self.generator.doFile(inputPath)
#         open(outputPath, 'w').write(self.generator.getResult())
#         
#     def convertSource(self, code, outputPath):
#         self.generator.doCode(code)      
#         open(outputPath, 'w').write(self.generator.getResult())
#         
#     def include(self, file):
#         code = open(file, 'r').read()
#         
#         exec(code, self.generator.workspace)
# 
#         
#     def expose(self, workspace):
#         # Exposed functions
#         workspace['CG_convertFile'] = lambda src, dst: self.convertFile(src, dst)
#         workspace['CG_convertSource'] = lambda src, dst: self.convertSource(src, dst)
#         workspace['CG_getArg'] = lambda arg: self.getArg(arg)
#         workspace['CG_getNumArgs'] = lambda : len(self.args[2:])
#         workspace['CG_write'] = lambda x: self.generator.write(x)
#         workspace['CG_include'] = lambda src: self.include(src)
#         
#     def doController(self, src, args):
#         self.args = args
#         
#         self.expose(self.generator.workspace)
#         
#         self.include(src)
        