Namespace
=========

.. module:: core.namespace
   :synopsis: Used for organizing tasks

.. class:: Namespace

   The Namespace class is used as a mini container between targets and tasks.
   They modify how tasks are spawned. A namespace is equivalent to a prefix for
   all tasks. For instance, if a task were to have a name of 'CXXCompile', then
   a namespace of 'cxx' would allow the spawning of a compile task underneath
   it.

   Creating your own namespace is as simple as inheriting from the main
   Namespace class located within core, and naming your namespace class as the
   prefix. A lower-case version of the name will be used. Also, make sure to
   that all tasks that use this name will have the namespace at the beginning
   of their name. (Such as CXXCompile, or CSharpCompile for cxx.compile or
   csharp.compile)
