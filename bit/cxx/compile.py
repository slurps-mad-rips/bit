from bit.core.task import Task

from bit.cxx.compiler import *

class CXXCompile(Task):
    
    compiler = CXX() # CXX is the 'platform default' compiler on import

    def __init__(self, *args):
        super().__init__(*args)
        self.attributes.update(dict(
            include=[],
            defines=[],
            flags=[]
        ))

    def execute(self):
        pass        
