# Bit of a 'hack' to ensure that the tasks are imported with a simple
# 'from bit import cxx' statement
# This kind of thing will most likely be used in other toolchain modules :/
from bit.cxx.configure import CXXConfigure
from bit.cxx.cxx import CXX
