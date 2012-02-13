# The Base Class for dependency information

import os

class Context(object):

    def __init__(self, name=str(), parent=None):
        self.dependencies = dict() # Must be a dict of Context inherited objs
        self.properties = dict()   # Used as a dictionary of user values
        self.order = list()        # The order in which dependencies are run

        self.description = str()   # Used for command line information
        self.parent = parent       # Let's us call up the dep graph
        self.name = name           # An optional name for command line options

        if parent: self.cache = os.path.join(parent.cache, self.name)

    def __setitem__(self, key, value): self.properties[key] = value
    def __getitem__(self, key): return self.properties[key]

    # Execution order is
    # 1) Is name an actual attribute?
    # 2) Is name a dependency?
    # 3) 'Spawn' an attribute
    def __getattr__(self, name):
        try: return object.__getattribute__(self, name)
        except AttributeError: pass
        try: dependencies = object.__getattribute__(self, 'dependencies')
        except AttributeError: dependencies = { }
        if name in dependencies: return dependencies[name]
        return self.spawn(name)

    def __enter__(self): return self

    # Contexts never 'clean up' in __exit__. Tasks shouldn't be executed
    # during the setup of a context, but executed by the runtime instead.
    def __exit__(self, *args):
        if not self.parent: return
        self.parent.dependencies[self.name] = self
        self.parent.order.append(self.name)

    def execute(self):
        pass

    def spawn(self, name):
        pass

    def run(self):
        for dep in self.order: self.dependencies[dep].run()
        self.execute()
