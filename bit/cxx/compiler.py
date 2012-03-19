# Contains classes for various C/C++/ObjC compilers
__all__ = ['GCC', 'Clang', 'MSVC', 'CXX']

from collections import OrderedDict
from functools import reduce
from operator import add

from bit.core.utility import Platform, flatten
from color import print

import subprocess
import json
import sys
import os

platform = Platform()
# Base compiler class
class Base(object):

    def __init__(self):
        self.executable = 'cc'
        self.default_flags = [ ]

    def prefix_flag(self, prefix, args, quotes=False):
        form_str = '{}"{}"' if quotes else '{}{}'
        return [form_str.format(prefix, args) for arg in flatten(args)]

    # Let's us add a bit of 'pre-setup' stuff for all compilers if we need to.
    # cache is the 'folder' where this occurs.
    # called in the task's execute folder, so cache should already exist.
    def setup(self, cache):
        pass

class GCC(Base):

    def __init__(self):
        super().__init__()
        self.executable = 'gcc'
        self.default_flags = ['-std=c++0x']

    def include(self, args): return self.prefix_flag('-I', args, quotes=True)
    def define(self, args): return self.prefix_flag('-D', args)

class Clang(GCC):

    def __init__(self):
        super().__init__()
        self.executable = 'clang'
        self.default_flags = ['-std=c++0x', '-stdlib=libc++']

class MSVC(Base):
    
    def __init__(self):
        super().__init__()
        self.executable = 'cl'
        self.version = 10 # VS2010 is currently the default.
        self.arch = 'x64' # selects the toolchain. x64 by default
        self.default_flags = ['/nologo']

    def include(self, args): return self.prefix_flag('/I', args, args)
    def define(self, args): return self.prefix_flag('/D', args)

    def setup(self, cache):
        for arch in ('x86', 'x64', 'ia64'): # supported architectures
            for vers in (9, 10, 11): # supported versions :)
                setup_file = os.path.join(cache, 'msvc{}{}'.format(vers, arch))
                if not os.path.isfile(setup_file):
                    try: cache_msvc_path(setup_file, vers, arch)
                    except KeyError: pass # KeyError not a priority
        cached = os.path.join(cache, 
                    'msvc{}{}'.format(self.version, self.arch))
        # OrderedDict lets us ensure the PATHs stay in the same order
        # Don't just set it right away, as the user may add items to the PATH.
        # TODO: Should consider putting this into its own function as well...
        # TODO: performing this kind of operation on _every_ variable
        # so that os.environ becomes a combination of itself and whatever is
        # stored in the file...
        with open(cached) as file:
            split = lambda x: x.split(os.pathsep)
            env_vars = json.loads(file.read())['PATH'], os.environ['PATH']
            odict = OrderedDict.fromkeys
            os.environ['PATH'] = os.pathsep.join(
                [path for path in odict(
                    reduce(add, map(split, env_vars))).keys() if path != ''])
        

class CXX(MSVC if platform.windows else (GCC if platform.linux else Clang)):
    pass

def cache_msvc_path(info_file, version, arch):
    tools = os.environ['VS{}0COMNTOOLS'.format(version)]
    path = os.path.join('..', '..', 'vc', 'vcvarsall.bat')
    batch = os.path.normpath(os.path.join(tools, path))

    process = subprocess.Popen(
            'cmd /c "{}" {} & set'.format(batch, arch),
            stdout=subprocess.PIPE,
            universal_newlines=True)
    output, errput = process.communicate()
    if errput: raise IOError('Could not generate MSVC info: {}'.format(errput))
    env_vars = {k.upper():v for k, v in [l.split('=') 
        for l in output.split('\n') if '=' in l]}
    with open(info_file, 'w') as file: file.write(json.dumps(env_vars))
