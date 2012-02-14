from nose.tools import eq_ as eq, ok_ as ok, istest, raises
from unittest import TestCase as Test

from bit.core.workspace import Workspace
from bit.core.target import Target
from bit.core.task import Task

import os

class TestTarget(Test):

    @istest
    def spawn(self):
        with Target('test', None) as target:
            target.cache = 'build'
            with target.task as task:
                eq(task.name, 'task')
            ok('task' in target.dependencies)
            eq(target.task, target.dependencies['task'])

    @istest
    @raises(TypeError)
    def dependency_order_error(self):
        with Target('test', None) as target:
            target.cache = 'build'
            target << 4

    @istest
    def dependency_order(self):
        with Workspace() as bit:
            with bit.test as test: pass
            with bit.test2 as test: pass
            bit.test << bit.test2
            ok('test2' not in bit.dependencies)
            ok('test2' not in bit.order)
            ok('test2' in bit.test.dependencies)
            ok('test2' in bit.test.order)
            ok(isinstance(bit.test.test2, Target))
