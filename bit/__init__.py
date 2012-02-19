from bit.core.workspace import Workspace
from bit.core.utility import pushd, flatten
from bit.core.color import error

import os

def main():
    with Workspace() as bit:
        directory = bit.args.directory
        #TODO: Remove this stupid 'pathable'.
        #      For some reason, the bit.args.file turns into a list
        #      if -f/--file is specified
        pathable = directory, bit.args.file
        bitfile = os.path.join(flatten(pathable))
        if not os.path.isfile(bitfile):
            raise IOError('{} could not be found'.format(bitfile))
        with pushd(directory):
            with open(bitfile) as bfile:
                debug = 2 if not bit.args.debug_mode else 0
                script = compile(bitfile.read(), bitfile, 'exec', flags=debug)
                # TODO: consider not actually placing this in a try-except :|
                try: exec(script, globals={ }, locals={'bit':bit})
                except Exception as e: error(e)
            bit.run()
