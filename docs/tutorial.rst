Tutorial
========

This document is a quick tour of how to use Bit, and its basic features.

  * :ref:`tutorial-what-is-bit`
  * :ref:`tutorial-hello-bit`
  * :ref:`tutorial-tasks`
  * :ref:`tutorial-target-dependencies`

.. _tutorial-what-is-bit:

What is Bit?
------------

Bit is a small set of modules that are used to create a build system. The core
of it is very small (only a few classes and utility functions), and tries to
avoid as much magic as possible (outside a metaclass or two ;]). It's focus
is on simplicity, with speed being important, but not *the* priority.

Specifically, Bit is a build system that allows a user to simply declare what
they want to have happen, and the dependency graph is taken care of for the
user.

It's so simple that it's possible to even use Bit in conjunction with other
task-based systems such as `fabric <http://fabfile.org>` (whose tutorial
inspired the layout for this one). Bit tries not to hold your hand. It's just
there to get stuff done for you, so that you don't have to worry about
what order files are being built in, and if they have changed or not.

Bit works a lot like Make, or Scons, or even waf, where you designate build
targets, and possibly create a series of dependencies on said targets (such
as requiring a library be built before an executable). However, bit does this
within the python language, and without using weird parser hacks. You get the
best of both worlds: A simple build system, and python's entire standard
library.

.. _tutorial-hello-bit:

Hello, Bit!
-----------

Enough about what bit is, let's jump in to what bit *does*!

A bitfile is the term used to describe a bit script. The contents of a bitfile
are not one where a series of functions are simply called. Instead, the entire
script is compiled, and executed by python.

Within every bitfile, the :class:`Workspace <core.workspace.Workspace>` object
is available. It's name is 'bit', and it is local to that specific file.

First, we need to create a :class:`Target <core.target.Target>`. Targets are
created using the with statement in python, and are spawned by name
from bit::

    with bit.build as build:
        pass

Now, bit doesn't actually have a target named ``build`` until we access it.
We're telling bit to create a target with whatever is named after it! This can
be done with anything that is a legal variable name in python::

    with bit.shirts as target:
        pass

    with bit.pants as target:
        pass

    with bit.shirt as target:
        pass

Now, when we go to run bit, we can either let all three of our defined targets
run (this is done by default), or we can specify a specific target::

    bit -t shirts

Now the ``shirts`` target will be run. However, we don't actually have anything
happening within the ``shirts`` target, so we should add a
:class:`Task <core.task.Task>`.

.. _tutorial-tasks:

Tasks
-----

Tasks are the bread and butter of actually getting things done within bit.
They are created in the same way as a Target, except that the name actually
matters. Let's assume there are two tasks: run, and Echo. run simply runs the
given arguments, and Echo prints text::

    with bit.shirts as target:
        with target.Echo as echo:
            echo.input = 'this text will be printed to the screen.'
        with target.run as run:
            run.input = 'echo this text will also be printed ;)'

.. note:: There are no run or Echo tasks currently provided in the bit core
          module. They are instead placed inside of the utility module, which
          is not yet written, or documented. This notice will be removed, and
          the tutorial updated when this is no longer the case.

Creating a task means we have to access the name of a task from the target.
Tasks shouldn't be run by the Workspace, but contained within a target.

So when we run::

    bit -t shirts

It will first call the Echo task, followed by the run task (which in this case
also calls echo). Defining your own tasks can be a little tricky, but that is
covered in :ref:`How To Write Your Own Task <howto-write-your-own-task>`.

Tasks of Tasks
^^^^^^^^^^^^^^

Tasks can also define other tasks. Say we wanted run to be run after Echo. We
can do it like so::

    with bit.shirts as target:
        with target.run as run:
            run.input = 'echo we're printing text!'
            with run.Echo as echo:
                echo.input = 'yes!'

In the above example, we would see 'yes!' followed by 'we're printing text!'.
Effectively, the most deeply nested ``with`` statement is executed before any
others.

Multiple Tasks of the Same Kind
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

But how can we have tasks that are of the same kind? If we wanted to do::

    with bit.shirts as target:
        with target.run as run:
            run.input = 'echo 1'
        with target.run as run:
            run.input = 'echo 2'

We would only ever see '2'. Instead, we need to rename the task internally
for the target::

    with bit.shirts as target:
        with target.run('run_1') as run:
            run.input = 'echo 1'
        with target.run as run:
            run.input = 'echo 2'

We should now see 1 and 2.

.. _tutorial-target-dependencies:

Target Dependencies
-------------------

Sometimes targets need to be run before others. This can cause an issue in some
cases where files may not be created, or copied to a proper location.

When a target has already been created by bit, it can be accessed again by name
like so::

    with bit.shirts as shirts:
        pass

    # Do some work down here

    some_function(bit.shirts)

This allows you to declare a target to be dependent on another (assuming the
target was already defined) with the following syntax::

    with bit.shirts as shirts:
        pass

    with bit.pants as pants:
        pants << bit.shirts

Now the ``shirts`` target will be run before ``pants``. Once this is done,
however, ``shirts`` is no longer accessible via ``bit``. Instead it must be
accessed via ``bit.pants.shirts``. This was done to encourage *not* creating
deeply nested dependencies. These are a bad thing in any build system. However,
bit doesn't try to hold your hand, so it doesn't stop you from doing it.

HOWEVER, in this case only will bit error if the type of the object on the
right is *not* a Target. Targets can only depend on tasks via ``with``, and
Targets via ``<<``.

And that's it! We've seen the actual very basics of bit.
