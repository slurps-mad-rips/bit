from contextlib import contextmanager
from functools import reduce
from operator import add

from bit.core.error import LocateError

import hashlib
import json
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

# Used to handle file list references being in tasks
class FileList(object):

    def __init__(self):
        self.output_list = []
        self.input_list = []

    @property
    def output(self): return self.output_list

    @property
    def input(self): return self.input_list

    @output.setter
    def output(self, value): self.output_list += flatten(value)

    @input.setter
    def input(self, value): self.input_list += flatten(value)

class Platform(object):
    def __init__(self):
        self.windows = True if sys.platform == 'win32' else False
        self.macosx = True if sys.platform == 'darwin' else False
        self.linux = True if 'linux' in sys.platform else False
        self.bsd = True if 'bsd' in sys.platform else False
        self.posix = self.macosx or self.linux or self.bsd

@contextmanager
def pushd(directory):
    if not os.path.exists(directory): raise LocateError(directory)
    old = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old)

def file_changed(name, data):
    orig_hash = int(data.get('hash', '0'), base=16)
    orig_time = int(data.get('time', 0))
    orig_name = data.get('name', None)

    if name != orig_name: return True
    # Should short-circuit the hash_file call.
    return time == orig_time and orig_hash == hash_file(name)

# Returns an int that is the MD5
def hash_file(name):
    with open(name, 'rb') as file:
        hash = int(hashlib.md5(file.read()).hexdigest(), base=16)
    return hash

def is_exe(path):
    return os.access(path, os.X_OK)

def flatten(container):
    if not isinstance(container, (list, tuple)): return [container]
    return reduce(add, map(flatten, container)) if container else []

# Will be removed so that pip's util.find_command function can be used
# instead.
def which(name):
    if sys.platform == 'win32' and not name.endswith('.exe'):
        name = '{}.exe'.format(name)
    path, _ = os.path.split(name)
    if path and is_exe(name): return name
    for path in os.environ['PATH'].split(os.pathsep):
        testable = os.path.join(path, name)
        if is_exe(testable): return testable
    raise LocateError(name)
