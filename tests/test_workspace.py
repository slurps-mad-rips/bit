from nose.tools import eq_ as eq, ok_ as ok, istest
from unittest import TestCase as Test

from bit.core.workspace import Workspace
from bit.core.target import Target

import os

class TestWorkspace(Test):

    @istest
    def args(self):
        with Workspace() as bit:
            eq(bit.args.file, 'bitfile')
            eq(bit.args.directory, os.getcwd())
            eq(bit.args.target, 'all')

    @istest
    def spawn(self):
        with Workspace() as bit:
            with bit.whatever as whatever:
                ok(isinstance(whatever, Target))
            eq(bit.whatever, bit.dependencies['whatever'])
