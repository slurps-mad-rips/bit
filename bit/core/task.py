from bit.core.utility import flatten
from bit.core.context import Context
from bit.core.color import error

import os

# Tasks get registed by using metatask as their metaclass
class MetaTask(type):
    lookup = { }

    def __new__(cls, name, bases, attrs):
        task = super().__new__(cls, name, bases, attrs)
        MetaTask.lookup[name.lower()] = task
        return task

    # TODO: Implement error handling for when a task can't be found
    @staticmethod
    def get(name) : return MetaTask.lookup[name]

# The base task class gets a bit hacky,
# because we overridde a lot of parent methods.
# This results in recursion otherwise :/
class Task(Context, metaclass=MetaTask):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.description = 'Base Task'

        # All attribute values MUST be a list.
        self.attributes = dict(input=[],#self.files.input,
                               output=[])#self.files.output)

    # On delete, the task's serialize method is called
    # Additional exceptions (such as IO) are reported by Python,
    # but ignored.
    def __del__(self):
        try: os.makedirs(os.path.normpath(self.cache), exist_ok=True)
        except OSError: error('Cannot create task cache {}'.format(self.cache))
        with open(os.path.join(self.cache, self.name), 'w') as cache:
            cache.write(self.serialize())

    # Called after dependencies, but BEFORE self.execute
    # data is whatever is in the contents of the file,
    # but the file must be readable in 'r' mode.
    def deserialize(self, data): pass

    # Must be implemented by child classes to save/cache info
    # No assumptions are made about outgoing or incoming data
    def serialize(self): return ''

    # Execcution order
    # 1) Does the requested name exist in our attributes dict?
    # 2) return object.__getattribute__
    def __getattr__(self, name):
        try: attributes = object.__getattribute__(self, 'attributes')
        except AttributeError: attributes = { }
        if name in attributes: return attributes[name]
        return super().__getattr__(name)

    # Execution order is
    # 1) Does the requested value exist in our custom attributes dict?
    # 2) Set the attribute of the instance dict.
    # TODO: fix the attributes so that a flatten isn't being applied every
    #       single time. This breaks the input/output listing.
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
        if os.path.isfile(cache_file):
            with open(cache_file, serialize_read_mode) as cache:
                self.deserialize(cache.read())
        self.execute()
