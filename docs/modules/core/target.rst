Target
======

.. module:: core.target
   :synopsis: Used for creating lists of tasks

.. class:: Target

  The Target class can be viewed as the kind of build target from a makefile.
  There is no limit to how many can be made, and they can be placed into
  a style of 'execution' order. This allows a dependency graph to be built
  without confusing syntax.

  Targets can spawn Tasks, and be dependent on each other. They work as a
  sort of 'safe' container between the :class:`core.workspace.Workspace` and
  the :class:`core.task.Task`

  .. function:: __lshift__(self, other)

     The overloading of the lshift operator results in dependencies between
     targets looking like so::

         with bit.target as target:
            target << bit.other_target

     This results in other_target now being a dependency of target, and it
     will now be run before target is. Care must be taken, as any tasks
     that are created before the inter-target dependency is created will be
     run. This was done as a lazy way to handle sorting of targets and tasks,
     but also allows for some tasks to be executed before a full target
     dependency is needed. When this is called, it will remove the
     dependent task from its parents execution list. This allows targets
     already depending on other targets to be reassigned without issue.

     :param other: The incoming dependent target
     :type other: Target
     :raises TypeError: If other is not of type Target

 
  .. function:: spawn(self, name)

     Spawns a :class:`core.task.Task` with the given name. This task is then
     placed into the target's execution list.

     :param name: The name of the task requested.
     :type name: str
     :raises KeyError: If the requested name cannot be found in the
                       :class:`core.task.MetaTask` internal lookup dict
