Bit Documentation
=================

Bit is a minimalistic, small, and simple build system. It tries to work like
waf or Scons in that it replaces the need of a Makefile. It isn't going to be
the fastest build system, but it will be faster than Scons, and easier to
understand.

Bit at its core is a small set of classes that allow a dependency graph to be
constructed simply by defining a project. It also allows the quick configuring
of a project.

With different toolchains, Bit becomes more powerful. As a matter of course,
it knows how to work with popular C and C++ compilers (such as clang, msvc,
and gcc), and easily supports cross compilation.

.. toctree::
   :maxdepth: 1

   Tutorial <tutorial>
   How To <howto/index>
   Design <design/index>
   Modules <modules/index>

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
