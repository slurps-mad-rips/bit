Task
====

.. module:: core.task
   :synopsis: Used for task-related functionality

.. class:: MetaTask

   All Tasks must use this as their metaclass. By using it as their metaclass,
   they are automatically registered for lookup.

   .. note:: If two task's names conflict, whichever one is registered second
             will be the one that is used when requested. This is due to the
             internal lookup dictionary that is used. This might cause
             conflicts for tasks which share a common name, such as 'compile'
             or 'link', however it is recommended that these tasks use the
             actual tool's name instead.

   .. staticmethod:: get(name)

      Returns the Task subclass from the internal dict. Names are lower-case
      in all instances.

      .. note:: This may change in a future release to allow the registration
                of upper case names.

      :param name: Name of task to get from the dictionary
      :type name: str

.. class:: Task

   A task is where a majority of work is done, and as such, is also where the
   actual meat of actual work is done.

   .. attribute:: attributes

      A dictionary of type { str : list }. These lists shouldn't be flattened,
      as it allows for an input and output reference to be placed within other
      tasks, and be updated without having to reset the references.

      By default, this holds the input and output lists. All members of
      attributes are accessed as though they were a part of the Task object.

   .. attribute:: description

      Currently unused, however this might be used in the future for a list
      option, and should be set by a task each time.

   .. method:: deserialize(data)
               serialize

      It is up to any specific task on how it serializes data between runs.
      As of right now, it will call serialize when the actual task is being
      garbage collected.

      .. note:: The serialize and deserialize methods are going to be changed
                such that they are simply called instead of performing the
                actual file IO. This will allow the task to serialize
                data however it wants, at the cost of additional complexity.
                
                On the other hand, this allows for serialization in whatever
                format is considered best, such as json, flat files, sqlite,
                or even xml.

   .. method:: __setattr__(name, value)

      An override of the __setattr__ method which allows statements such as::

          task.input = 1, 2, 3, 4
          task.input = 2, 3, 4, 5

      To not result in data being overwritten. Additionally, anything that goes
      'in' to an attribute is not flattened until the user requests it.

      .. note:: This is not what actually happens at this moment in time.
                It will be fixed shortly.
