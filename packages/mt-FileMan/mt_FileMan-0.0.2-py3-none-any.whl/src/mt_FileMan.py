import sys
import pathlib
from datetime import datetime

import re

import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

class mtIOMan(object):

    def __init__(self): 
        super().__init__() 

    def startLog(self, logLevel=0):
    
        theCurrentDatetime = datetime.now()
        #Make dir if not exist (python 3.5+), use pathlib2 < 3.5
        pathlib.Path('LOG').mkdir(parents=True, exist_ok=True)
        pathlib.Path('UI').mkdir(parents=True, exist_ok=True) 
        logFN = 'LOG/log_'+theCurrentDatetime.strftime("%Y-%m-%d_%H-%M-%S")+'.log'
        f = open(logFN, 'w')
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, f)
        
        return f
        
    def sorted_nicely( l ): 
        """ Sort the given iterable in the way that humans expect.""" 
        convert = lambda text: int(text) if text.isdigit() else text 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(l, key = alphanum_key)

if __name__ == '__main__':
    from datetime import datetime

    theCurrentDatetime = datetime.now()
    today = theCurrentDatetime.strftime('%Y-%m-%d')
    print('Today\'s date is: '+today)
