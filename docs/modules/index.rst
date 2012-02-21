Bit Modules
===========

The modules provided with Bit are the core module, where all basic logic stems,
and the cxx module, which contains types for a C/C++/ObjC toolchain.

The core module's documentation contains information on the actual internal
workings of bit. The other modules documentation shows a list of tasks,
and their use as well as expected behavior.

.. toctree::
   :maxdepth: 1

   Core <core/index>
   C++ <cxx/index>

Bit
---

The Bit program is provided as a script that will execute a given bitfile.

.. program:: bit

.. option:: -f <file>, --file <file>

   The file to use as the bitfile. The default value is 'bitfile'. The
   bitfile must be a python script that will compile properly. Errors that
   exist from either running a python script or compiling one will
   be passed back through bit, with a proper traceback.

.. option:: -d <directory>, --directory <directory>

   The directory to find the bitfile in. This is also where bit will execute
   from, before returning to the original starting directory.

.. option:: -t <target>, --target <target>

   Names the specific target to run. This will also run any dependencies that
   the target depends on. By default, it will run all targets.

.. option:: --debug-mode

   Compiles the bitfile with the debug flag settings. This is not recommended
   unless black magic is being practiced within a user's bitfile.

.. option:: --show-options

   Works like --help, except it will show all user-defined options as well.

.. note:: Using :option:`bit --show-options` requires a bitfile to be read
          from. If it cannot be found, then the IOError will be raised.

.. option:: --version

   Prints the current version of bit (with the named release).

.. option:: --help

   Prints the above options, as well as user-defined options.
