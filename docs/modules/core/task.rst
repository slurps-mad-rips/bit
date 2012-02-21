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

   .. attribute:: deserialization

      A dictionary which contains the values used for json-decoding. The values
      should be key-value pairs equivalent to the arguments passed into
      ``json.loads``

   .. attribute:: serialization

      A dictionary which contains the values used for json-encoding. The values
      should be any object which can be sent to json.dumps for serialization.

   .. method:: deserialize(data)

      When a task is deserialized, the contents of its cache file will be read
      into memory, and then decoded with the python JSON module. The resulting
      object is then passed in to deserialize. Any options related to the
      decoding of JSON should be modified with the deserialization attribute
      dictionary.

      This method is called after dependencies, but BEFORE the task actually
      executes.

      :param data: Object deserialized from JSON.

   .. method:: serialize

      Serialize is called before the Task is actually garbage collected,
      and should return a JSON encodable object. Any options related to the
      encoding of JSON should be placed in the serialization attribute
      dictionary.

      :returns: A JSON Encodable object, such as a list, dict, etc.

   .. method:: __setattr__(name, value)

      An override of the __setattr__ method which allows statements such as::

          task.input = 1, 2, 3, 4
          task.input = 2, 3, 4, 5

      To not result in data being overwritten. Additionally, anything that goes
      'in' to an attribute is not flattened unless the task tells it to.

   .. method:: __getattr__(name):
      
      Returns the attribute located in the task by name.
      Execution order is

        1. Does the requested name exist in our attributes dict?
        2. Call Context.__getattr__(name)

   .. method:: __call__(name)

      :param name: the new name with which to refer to the task by.
      :type name: str

      This is used to change the name of a task, to workaround being unable to
      run multiple tasks with the same name. Because of the order in which
      tasks are registered to their parent, using the ``__call__`` method
      before exiting the with context will change the name.

   .. method:: __del__
      
      Calls :meth:`core.task.Task.serialize` when the object is destructed.
      First creates the tasks 'cache' folder.

      .. warning:: Take care when debugging, or throwing exceptions during
                   anything called during __del__. The CPython implementation
                   ignores these, and exits regardless.

   .. method:: spawn(name)

      :param name: Name of the task to lookup from :class:`core.task.MetaTask`.
      :type name: str

      Works in the exact same way as :class:`core.target.Target`. This results
      in tasks being capable of spawning others that are dependent on them.
