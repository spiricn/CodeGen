import os

class FileSystemIncludeHandler:
    def __init__(self):
        self.__locations = []
        
    def addSearchPath(self, location):
        self.__locations.append( location )
        
    def getIncludeContent(self, file):
        for location in self.__locations:
            for directory, dirNames, fileNames in os.walk(location):
                for i in fileNames:
                    if i == file:
                        file = open(os.path.join(directory, i), 'r')
                                                
                        content = file.read()
                        
                        content = content.replace('\r', '')
                        
                        file.close()
                        
                        return content

        return None