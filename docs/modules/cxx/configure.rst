Configure
=========

.. module:: cxx.configure
   :synopsis: The cxx module's configure task, primarily for headers.

.. class:: CXXConfigure

   The cxx configure class relies on the Mako templates for handling changes,
   as well as inputs, outputs, and 'rendering'. While Mako was designed and is
   primarily used for the web, its templating system (and syntax) makes it
   extremely viable for general development on many platforms, and in many
   languages. The configure task, therefore, is a simple wrapper around the
   primary functionality of a Mako template.
