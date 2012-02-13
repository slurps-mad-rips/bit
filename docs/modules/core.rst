Core
====

.. module:: core
   :synopsis: The central and most important module

The core module provides a number of basic types as well as a few utility
functions.

 * :mod:`utility <core.utility>`
 * :mod:`color <core.color>`
 * :mod:`context <core.context>`

core.utility
------------

Various functions and types. Among these, the flatten function should be noted.
It allows the simple appending of lists and tuples to lists (rather than adding
them) and can be a bit faster in terms of grabbing data for later use.

.. module:: core.utility
   :synopsis: miscellaneous types and functions

.. class:: Platform

   A simple object that allows platform lookup with simple getter attributes.
   (e.g., ``if platform.windows:``)

   .. attribute:: windows
                  macosx
                  linux
                  bsd

   The available platform hosts that bit currently targets or supports.
   All provided attributes are booleans unless stated otherwise.

.. function:: pushd(directory)

   Used in a with statement, and works like the shell pushd command. This
   allows a user to temporarily enter and exit a directory without having
   to manually store the original working directory.

   :param directory: A string representing either a relative or full path
   :raises LocateError: When directory does not exist or can't be entered

.. function:: is_exe(path)

   Examines whether the given path is executable or not

   :return: False if the path doesn't exist or isn't executable, otherwise True

.. function:: which(name)

   Works like the which utility in posix. However, it only ever returns the
   first possible match. On windows, a '.exe' extension will be appended. This
   means that batch files and other non .exe files are not usable for tools.

   :param str name: The name of the executable to find.
   :raises LocateError: If the given name cannot be found on the system path.

.. function:: flatten(container)

   Flattens the given container (and the elements contained within) into
   a single list.

   :param container: A list or tuple type.
   :type container: list or tuple
   :return: A single list containing all elements within container

core.color
----------

Simple color printing utilities

.. module:: core.color
   :synopsis: Color printing functions

.. function:: command(msg)
              warning(msg)
              success(msg)
              error(msg)
              info(msg)

   Prints the given msg to either stdout or stderr. The colors used (in order
   of function declaration) are:

   * magenta
   * yellow
   * green
   * red
   * cyan

   :param str msg: string to print

core.context
------------

.. module:: core.context
   :synopsis: base class for dependency graph building.

.. class:: Context

   A Context represents a python context manager scope as well as the basic
   dependency building block in bit. This class makes the entire system
   *extremely* flexible. However it causes actual file dependency tracking to
   be handled by individual tasks defined within bit.

   The __getitem__ and __setitem__ overloads are provided to allow for
   user-defined information that can be stored at any scope. (In this sense,
   the term 'user-defined' is anyone not extending bit, but instead creating
   an actual bitfile)

   Contexts should be used as a context scope would be in python. Using a with
   statement not only helps organize code, but also results in a proper
   dependency graph being built. Accessing a context's attribute will result
   in a Context inherited object being returned. If the requested attribute
   does not yet exist, it will be generated. For instance::

      with context.newer as newer:
        with newer.whatever as whatever:
          pass
      print(context.newer.whatever)
   
   In the above example, the 'newer' attribute doesn't exist when it is first
   accessed, but is still available after exiting the context scope. When the
   context's 'run' method is called, it will first call newer's run method,
   which in turn calls whatever's run method, and so on and so forth. As long
   as there is a 'child' for a given Context, it will be run before the parent.

   .. attribute:: dependencies

      A dictionary of string:Context pairs. These are contexts that will be run
      before the active context.

   .. attribute:: properties

      A dictionary to store additional user-defined values in.

   .. attribute:: order

      The order of dependencies to execute. This is a list of strings which
      are equal to the keys located in the dependencies dict.

   .. attribute:: parent

      The parent is the parent context. This is set during the 'spawn' function
      usually.

   .. attribute:: description

      An optional string which is used for command-line option information.

   .. attribute:: cache

      string pointing to a filesystem path, based on the parent's cache value
      Contexts without a parent must manually set their cache before spawning
      any dependent contexts.

   .. attribute:: name

      The name of the Context. This is generated if not provided in some cases,
      and in many cases is not 'nameable' (where the name of the Context is
      also the name of a task)

   .. method:: execute(self)

      Actual work for a given Context should be placed in an override of
      execute. By default execute does nothing.
   
   .. method:: spawn(self)

      Called by the __getattr__ method to create a new Context inherited
      object. This is also only ever called internally, but should be overriden
      for custom classes. By default, spawn does nothing.

   .. method:: run(self)

      This method is only ever called internally, and it is recommended that
      types outside of core do not override it.
