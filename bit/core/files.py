# FileList and FileNode classes

# Used for tasks where the input or output files
# shouldn't be cached for changes.
class TempNode(object):
    def __init__(self, name):
        self.name = name
        self.changed = True

class FileNode(object):
    def __init__(self, name, data):
        self.hash = int(data.get('hash', 0), base=16)
        self.time = int(data.get('time', 0))
        self.deps = data.get('deps', []) # Filenames that depend on this one
        self.name = name
        self.changed = False

        self.check()

    def serialize(self):
        return {
            self.name : {
                'deps' : self.deps,
                'time' : self.time,
                'hash' : self.hash
            }
        }

class FileList(object):
    def __init__(self):
        self.output = [ ]
        self.input = [ ]
