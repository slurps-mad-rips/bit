from bit.core.utility import *
from bit.core.error import LocateError

from nose.tools import ok_ as ok, eq_ as eq, raises, istest

from unittest import TestCase as Test, skipIf as skip_if

import sys
import os

class TestWhich(Test):

    @istest
    def python(self):
        eq(sys.executable, which(sys.executable))

    @istest
    @raises(LocateError)
    def unknown(self):
        which('some executable name that you will never ever have')

class TestFileList(Test):

    def __init__(self, *args):
        super().__init__(*args)
        self.files = FileList()

    @istest
    def input(self):
        self.files.input = 1, 2, 3, 4, 5
        eq(self.files.input, [1, 2, 3, 4, 5])
        z = self.files.input
        eq(z, [1, 2, 3, 4, 5])
        self.files.input = 2, 3
        eq(self.files.input, z)
        eq(z, [1, 2, 3, 4, 5, 2, 3])

class TestPlatform(Test):

    def __init__(self, *args):
        super().__init__(*args)
        self.platform = Platform()

    @istest
    def windows(self):
        eq(self.platform.windows, sys.platform == 'win32')

    @istest
    def macosx(self):
        eq(self.platform.macosx, sys.platform == 'darwin')

    @istest
    def linux(self):
        eq(self.platform.linux, 'linux' in sys.platform)

    @istest
    def bsd(self):
        eq(self.platform.bsd, 'bsd' in sys.platform)

    @istest
    @skip_if(sys.platform == 'win32', 'Always fails on windows')
    def posix(self):
        ok(self.platform.linux or self.platform.macosx or self.platform.bsd)
        ok(self.platform.posix)

class TestFlatten(Test):

    @istest
    def flatten(self):
        eq([1, 2, 3, 4, 7, 8, 9], flatten((((1, 2, 3), 4), [7, [8, [9]]])))

class TestPushd(Test):

    @istest
    def pushd(self):
        current = os.getcwd()
        parent, _ = os.path.split(current)
        with pushd(parent): eq(os.getcwd(), parent)
        eq(os.getcwd(), current)
