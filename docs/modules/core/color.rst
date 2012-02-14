Color
=====

The color module is simple in its use, but more complex in its implementation,
and as such exists within its own module. The color module simply provides
an easy way to print colored text to a commandline interface. No more, no less.

.. module:: core.color
   :synopsis: Color printing functions

.. function:: command(msg)
              warning(msg)
              success(msg)
              error(msg)
              info(msg)

   Prints the given msg to either stdout or stderr. The colors used (in order
   of declaration) are:

   * magenta
   * yellow
   * green
   * red
   * cyan

   :param str msg: string to print
