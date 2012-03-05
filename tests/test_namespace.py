from nose.tools import eq_ as eq, ok_ as ok, istest
from unittest import TestCase as Test

from bit.core.namespace import Namespace
from bit.core.target import Target

class TestNamespace(Test):

    @istest
    def spawn(self):
        with Target('test', None) as target:
            target.cache = 'build'
            with target.namespace as namespace:
                eq(namespace.prefix, 'namespace')
                eq(namespace.name, 'namespace')
