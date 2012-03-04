from bit.core.task import Task

from string import Template

# Currently VERY specific in how it works Oof :/
# TODO: Make it easier to modify
# NOTE: VERY BROKEN ATM
class CXXConfigure(Task):
    '''
    # On change will result in self.execute being run
    def deserialize(self, data):
        # First check for files that have changed
        for file in self.input.files:
            pass
            #data[file]

        # Then check actual property values
        if data['properties'] != self.properties:
            pass

    #TODO: fix to hold more information
    def serialize(self): return self.properties

    def execute(self):
        if not self.changed: return
        with open(self.files.input[0]) as file:
            template = Template('\n'.join([self.fix(line) for line in file]))
        # Not accurate filepath
        with open(self.files.output[0], 'w') as file:
            file.write(template.safe_substitute(self.properties))


    def fix(self, line):
        line = line.lstrip()
        if not line.startswith('`'): return line
        line = line.replace('`define', '#define')
        size = line.split(' ')[1:]
        if size == 1:
            # boolean expression
            pass
        else:
            # continue on
            pass
        return line
    '''
