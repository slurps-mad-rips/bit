# A 'wrapper' task object that allows toolchains to spawn consistently named
# tasks.

from bit.core.task import Task

class Namespace(Task):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.prefix = self.__class__.__name__

    # The prefix doesn't matter in terms of capitalization because
    # the MetaTask.get method will use the .lower() call to create it
    def spawn(self, name):
        return MetaTask.get('{}{}'.format(self.prefix, name))(name, self)
