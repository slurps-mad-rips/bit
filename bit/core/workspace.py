# The 'bit' object available in all bitfiles.
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from bit.core.utility import Platform, Option
from bit.core.context import Context
from bit.core.target import Target

import os

class Workspace(Context):

    # These being built doesn't really matter
    platform = Platform()
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        conflict_handler='resolve',
        fromfile_prefix_chars='@'
    )


    def __init__(self):
        super().__init__('bit', None)

    # Workspace is only ever instantiated once (in the main function)
    # and then passed into the resulting bitfile via exec.
    # We take this time to setup the initial argument information.
    # The basic use of Workspace is basically
    # 'with Workspace() as bit: exec(bit.options.file, etc. etc.)'
    def __enter__(self):
        add_argument = self.parser.add_argument
        add_argument('--version', action='version', version='bit 0.4-2112')
        add_argument('-f', '--file', nargs='?', type=str, default='bitfile',
                     help='build script to use')
        add_argument('-d', '--directory', nargs='?', type=str,
                     default=os.getcwd(), help='root execution directory')
        add_argument('-t', '--target', nargs='?', type=str,
                     default='all', help='target to run')
        add_argument('--debug-mode', action='store_true', default=False,
                     help='bitfile is compiled with debug flags')
        add_argument('--show-options', action='store_true', default=False,
                     help='prints all help, including user defined options')
        self.args, _ = self.parser.parse_known_args()
        # Initializing before a first-parse results in this showing up empty
        self.options = Option(self)
        self.cache = os.path.join(self.args.directory, '.bit')
        return self

    # Loads a file, then runs it in isolation from the current environment
    def load(self, name):
        path = os.path.join(self.args.directory, name)
        if not os.path.isfile(path):
            raise IOError('{} is not a file'.format(path))
        with open(path) as bfile:
            debug = 2 if not bit.args.debug_mode else 0
            script = compile(bfile.read(), path, 'exec', optimize=debug)
            exec(script, { }, {'bit': self })


    def spawn(self, name): return Target(name, self)

    # Modified
    def run(self):
        if self.args.target == 'all':
            for dep in self.order: self.dependencies[dep].run()
        else: self.dependencies[self.args.target].run()
