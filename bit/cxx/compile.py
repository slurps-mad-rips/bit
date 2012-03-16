from bit.core.task import Task

class CXXCompile(Task):
    
    compiler = None # Currently don't have a default compiler set...

    def __init__(self, *args):
        super().__init__(*args)
        self.attributes.update(dict(
            cxxflags=[],
            include=[],
            library=[],
            defines=[],
            cflags=[],
            flags=[]
        ))
