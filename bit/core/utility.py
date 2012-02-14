from contextlib import contextmanager
from functools import reduce
from operator import add

from bit.core.error import LocateError

import sys
import os

# For user-defined options
class Option(object):
    def __init__(self, parent):
        self.parent = parent
        self.args = parent.parser.add_argument_group('Options', 'User Defined')
        self.arguments = { }

    def __getattr__(self, name):
        if name in self.arguments: return name
        raise AttributeError('{} is not a valid option name'.format(name))

    def set(self):
        temp, _ = self.parent.parser.parse_known_args()
        self.arguments.update(temp.__dict__)

    def add_argument(self, *args, **kwargs):
        self.args.add_argument(*args, **kwargs)
        self.set()

    def add(self, name, default=False, help=None):
        self.add_argument(
            '--{}'.format(name),
            action='store_true',
            default=default,
            help=help
        )
        

class Platform(object):
    def __init__(self):
        self.windows = True if sys.platform == 'win32' else False
        self.macosx = True if sys.platform == 'darwin' else False
        self.linux = True if 'linux' in sys.platform else False
        self.bsd = True if 'bsd' in sys.platform else False

@contextmanager
def pushd(directory):
    if not os.path.exists(directory): raise LocateError(directory)
    old = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old)

def is_exe(path):
    return os.access(path, os.X_OK)

def flatten(container):
    if not isinstance(container, (list, tuple)): return [container]
    return reduce(add, map(flatten, container)) if container else []

def which(name):
    if sys.platform == 'win32': name = '{}.exe'.format(name)
    path, _ = os.path.split(name)
    if path and is_exe(name): return name
    for path in os.environ['PATH'].split(os.pathsep):
        testable = os.path.join(path, name)
        if is_exe(testable): return testable
    raise LocateError(name)
