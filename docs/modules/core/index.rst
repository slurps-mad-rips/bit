Core Module
===========

.. module:: core
   :synopsis: The central and most important module

The core module provides a number of basic types as well as a few utility
functions. It is also where every other module in bit (those included or
those being written externally) takes its basic behavior from.

The core of bit is actually very small, and something complex such as
dependency tracking is instead left up to the implementer of a given task.
This can cause issues where a dependency handling system for a toolchain,
such as a C/C++ compiler where the dependency tracking can be a little complex,
however it takes the burden off of bit for how files should be tracked, and
metadata stored.

.. toctree::

   workspace
   target
   task
   context
   utility
   color
