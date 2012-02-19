Workspace
=========

.. module:: core.workspace

.. class:: Workspace

   There is only ever one Workspace instance when bit is running. It is located
   within the variable named 'bit' and will be available within the bitfile.
   The Workspace is where all user-declared targets are registered, and then
   run. It is also how targets are created (via the with statement)

   The workspace is also where the central 'utility' objects are placed (such
   as :class:`core.utility.Platform` and :class:`core.utility.Option`.

   There should only ever be one workspace instance, and it shouldn't ever be
   created multiple times, or have it's :class:`core.workspace.Workspace.run`
   method called before the end of the bitfile.
