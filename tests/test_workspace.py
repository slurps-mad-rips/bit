
from nose.tools import eq_ as eq, istest
from unittest import TestCase as Test

class TestWorkspace(Test):

    @istest
    def failure(self):
        self.fail('not yet implemented')
