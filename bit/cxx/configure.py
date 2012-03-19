from bit.core.task import Task

from mako.template import Template

# Mako has a GREAT templating language that is actually really easy to apply to
# more than just HTML. It's also available via pip, and works with python 3,
# so we can take advantage of that.

# The mako templates use a caching system which we take advantage of to
# see if we need to regenerate anything. Saves us time!
class CXXConfigure(Task):

    # TODO: Handle errors from the task.
    def execute(self):
        with open(self.output[0], 'w') as file:
            template = Template(filename=self.input[0],
                                module_directory=self.cache)
            file.write(str(template.render(**self.properties)))
