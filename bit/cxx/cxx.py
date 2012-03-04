# The 'cxx' task is a magic task, in that it modifies how tasks are spawned
# within the cxx module, using a 'shortcut' route. All actual tasks in
# bit.cxx are prefixed with CXX. The CXX task allows for something like:
#
# with target.cxx.compile as compiler:
#   pass

from bit.core.namespace import Namespace

class CXX(Namespace): pass
