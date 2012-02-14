Utility
=======

The utility module contains various functions and types that can't be placed
into a specific category. These range from simple 'macro' functions, such
as :func:`core.utility.is_exe` to more complex functions such as
:func:`core.utility.flatten`. There are also functions provided to help
with the implementation of tasks.

.. module:: core.utility
   :synopsis: miscellaneous types and functions

.. class:: Option

   The option class is used by :class:`core.workspace.Workspace` for storing
   user declared command line options. The results of these options are
   accessed in the same way as if the resulting parsed arguments object was
   being accessed. This allows for a simple kind of access, such as
   ``if options.release`` and similar constructs. Additionally, arguments are
   only parsed when one is added to the internal argument parser. This allows
   for an option to be declared, and then have its value immediately checked,
   without requiring bit to know all options at before it invokes the bitfile.

   The way with which the arguments are parsed is less than ideal.
   Currently, all arguments are reparsed from the original values passed
   in. This could be routed by only parsing the remaining arguments,
   however it was decided that disallowing the overwriting of
   arguments once parsed would be beneficial.

   .. function:: add_argument(self, args, kwargs)

      A simple wrapper around the internal argument parser, which adds the
      argument internally, and then sets the argument value depending on what
      can be parsed from the arguments passed in to bit.

   .. function:: add(self, name, default=False, help=None)

      A shortcut for a small boolean option. Useful for small feature checks
      such as ``with-feature`` or ``enable-x``

.. note:: When adding a boolean option with a hyphen in the name, the argparse
          module will automatically turn it into an underscore when parsed.

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
   a single list. As of right now, no limit of the maximum number of elements
   that can be nested within a container has been found. As of right now,
   flatten can flatten any container as long as creating the nested container
   does not also result in a stack error. (That is, Python will error from
   creating too large a container before flatten can even get to it)

   :param container: A list or tuple type.
   :type container: list or tuple
   :return: A single list containing all elements within container
