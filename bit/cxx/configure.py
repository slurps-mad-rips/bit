from bit.core.color import error
from bit.core.task import Task

from mako.template import Template

# The mako templates use a caching system which we take advantage of to
# see if we need to regenerate anything. Saves us time!
class CXXConfigure(Task):

    # TODO: Handle errors from the task.
    def execute(self):
        with open(self.output[0], 'w') as file:
            template = Template(filename=self.input[0],
                                module_directory=self.cache)
            file.write(str(template.render(**self.properties))
