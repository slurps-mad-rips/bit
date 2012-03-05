from bit.core.task import *

from nose.tools import ok_ as ok, eq_ as eq, istest

from unittest import TestCase as Test, skipIf as skip_if

import sys
import os

class TestTask(Test):

    @istest
    def name(self):
        with Task('my_task', None) as task:
            task.cache = 'build'
            eq(task.name, 'my_task')
            with task.task('my_task2') as task2:
                eq(task2.name, 'my_task2')

    @istest
    def description(self):
        with Task('my_task', None) as task:
            task.cache = 'build'
            eq(task.description, 'Task')

    @istest
    def parent(self):
        with Task('my_task', None) as task:
            task.cache = 'build'
            eq(task.parent, None)
            with task.task as task2:
                eq(task2.parent, task)

    @istest
    def input(self):
        with Task('my_task', None) as task:
            task.cache = 'build'
            task.input = (((1, 2, 3), 4), [7, [8, [9]]])
            eq(task.input, [1, 2, 3, 4, 7, 8, 9])
