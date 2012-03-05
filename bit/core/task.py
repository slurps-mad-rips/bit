from bit.core.utility import flatten, FileList
from bit.core.context import Context
from bit.core.color import error

import json
import os

# Tasks get registed by using metatask as their metaclass
class MetaTask(type):
    lookup = { }

    def __new__(cls, name, bases, attrs):
        task = super().__new__(cls, name, bases, attrs)
        MetaTask.lookup[name.lower()] = task
        return task

    @staticmethod
    def get(name):
        try: return MetaTask.lookup[name]
        except KeyError as e:
            error('could not find task: {}'.format(e))
            raise # rethrow KeyError

# A bit hacky because we override a lot of Context methods
class Task(Context, metaclass=MetaTask):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.description = self.__class__.__name__
        self.deserialization = { }
        self.serialization = { }
        self.changed = False # currently unused :/
        self.files = FileList()
        self.file = os.path.join(self.cache, self.name)

        # All attribute values MUST be a list, as incoming values are
        # sent through flatten, and then +='d to the list
        self.attributes = dict(output=self.files.output,
                               input=self.files.input)
    
    def __del__(self):
        try: os.makedirs(os.path.normpath(self.cache), exist_ok=True)
        except OSError: error('Cannot create task cache {}'.format(self.cache))
        with open(self.file, 'w') as cache:
            cache.write(json.dumps(self.serialize(), **self.serialization))

    def deserialize(self, data): pass
    def serialize(self): return [ ]

    # Execcution order
    # 1) Does the requested name exist in our attributes dict?
    # 2) return Context.__getattr__
    def __getattr__(self, name):
        try: attributes = object.__getattribute__(self, 'attributes')
        except AttributeError: attributes = { }
        if name in attributes: return attributes[name]
        return super().__getattr__(name)

    # Execution order is
    # 1) Does the requested value exist in our custom attributes dict?
    # 2) Set the attribute of the instance dict.
    def __setattr__(self, name, value):
        try: attributes = object.__getattribute__(self, 'attributes')
        except AttributeError: attributes = { }
        if name not in attributes: object.__setattr__(self, name, value)
        else: attributes[name] += flatten(value)

    # Allows stuff like 'with task_that_already_exists('new_name') as new:
    def __call__(self, name):
        self.name = name
        return self

    def spawn(self, name):
        return MetaTask.get(name)(name, self)

    # Modified from the default so that we can deserialize at the right moment
    def run(self):
        for dep in self.order:self.dependencies[dep].run()
        cache_file = os.path.join(self.cache, self.name)
        if os.path.isfile(self.file):
            with open(self.file) as cache:
                self.deserialize(json.loads(cache.read(),
                                            **self.deserialization))
        self.execute()
