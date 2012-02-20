Workspace
=========

.. module:: core.workspace
   :synopsis: The workspace contains the actual 'global' bit instance.

.. class:: Workspace

   There is only ever one Workspace instance when bit is running. It is located
   within the variable named 'bit' and will be available within the bitfile.
   The Workspace is where all user-declared targets are registered, and then
   run. It is also how targets are created (via the with statement)

   The workspace is also where the central 'utility' objects are placed (such
   as :class:`core.utility.Platform` and :class:`core.utility.Option`.

   .. function:: __enter__(self)

      When the Workspace has its instance created it sets up the basic argument
      parser, as well as user options object. This function is never called by
      the user, and is only ever used within :func:`main`.

   .. function:: load(self, name)

      Runs a file as a script, but in isolation from the current environment,
      with the exception of the Workspace instance. This method is first called
      when the bitfile is first executed. And can be used to load other files
      (and execute them) on the fly. This method is available to ALL scripts
      that have the bit instance located within them.

      Additionally, the files loaded are compiled with whatever the
      :option:`bit --debug-mode` setting is.

      :param name: The path to the requested file.
      :type name: str
      :raises IOError: When name is not a file, or cannot be found
   

   .. function:: spawn(self, name)

      :param name: Name of the requested target. Should be a legal identifier
      :type name: str

      The workspace can only ever spawn :class:`core.target.Target`.
      These targets have the name requested, and the actual Workspace as their
      parent.

