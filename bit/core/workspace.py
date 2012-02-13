# The 'bit' object available in all bitfiles.
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from bit.core.utility import Platform
from bit.core.context import Context
from bit.core.target import Target

class Workspace(Context):

    def __init__(self):
        super().__init__('bit', None)
        self.platform = Platform()

    # Workspace is only ever instantiated once (in the main function)
    # and then passed into the resulting bitfile via exec.
    # We take this time to setup the initial argument information.
    # The basic use of Workspace is basically
    # 'with Workspace() as bit: exec(bit.options.file, etc. etc.)'
    def __enter__(self):
        self.parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter,
            conflict_handler='resolve',
            fromfile_prefix_chars='@'
        )
        add_argument = self.parser.add_argument
        add_argument('--version', action='version', version='bit 0.4-2112')
        add_argument('-f', '--file', nargs=1, type=str, default='bitfile',
                     help='build script to use')
        add_argument('-d', '--directory', nargs=1, type=str,
                     default=os.getcwd(), help='root execution directory')
        add_argument('-t', '--target', nargs='+', type=str,
                     default='all', help='target to run')
        self.options = Option(self)
        self.args, = self.parser.parse_known_args()

    def spawn(self, name): return Target(name, self)
