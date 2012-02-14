Context
=======

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

      Called when an instance is unable to find an attribute already within
      its class, or within the dependencies dict. By default it does nothing,
      and should only be modified in special cases such as core modules.

      However this does not mean that overriding it is out of the question.

   .. method:: run(self)

      This method is only ever called internally, and it is recommended that
      types outside of core do not override it.
