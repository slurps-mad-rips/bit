from bit.core.task import Task

from string import Template

# Currently VERY specific in how it works Oof :/
class CXXConfigure(Task):

    def deserialize(self, data):
        # check actual properties for changes
        if data['properties'] == self.properties: return

        name = self.input[0]
        time, hash = data[name]
        # TODO: get the only input file
        #if data['input'] == self.input[0]
            
    def serialize(self): pass
    def execute(self): pass

    def fix(self, line): pass
    '''
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
