import sys

from Controller import Controller

if __name__ == '__main__':
    sys.argv += ["example/example.py", "test"]
    
    if len(sys.argv) <= 1:
        print('Usage: python CodeGen.py <generator_file>')
        exit()
        
    ctrlPath = sys.argv[1]
    
    ctrl = Controller();
    
    ctrl.doController(ctrlPath, sys.argv)
    
    print('Done')
    
    
