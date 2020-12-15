Getting started
===============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Nothing fancy here, we just create a simple cli calculator with ``argparse_action``.

Single function
---------------

.. code-block:: python

   "Simple calculator"

   import argparse
   import argparse_action

   def add(a, b):
       print(a + b)

   parser = argparse.ArgumentParser(description=__doc__)
   argparse_action.add_action(parser, add)

   namespace = parser.parse_args()
   namespace.action(namespace)

The ``argparse_action.add_action`` does two things:

- defines cli arguments from the function signature of ``calc``
- register a wrapped function from ``calc`` into the parser as ``action``
  so ``namespace.action(namespace)`` will unwrap the paramaters from
  ``namespace`` and calls ``calc`` as a normal python function.

So a usual argparse help is available:

.. code-block::

   $ python3 calc.py -h
   usage: calc.py [-h] a b

   Simple calculator

   positional arguments:
     a
     b

     optional arguments:
       -h, --help  show this help message and exit

Let see how the script works:

.. code-block::

   $ python3 calc.py 1 2
   12

This is stranger! We should handle the arguments as numbers instead of strings.

The type annotation will help:

.. code-block:: python

   def add(a: int, b: int):
       print(a + b)

``argparse_action`` registers the type annotation of the parameters as the type
of the cli argument.

.. code-block::

   $ python3 calc.py 1 2
   3

**Remark:** You should use such types which accept str as input.

Multiple commands
-----------------

We should extend ``calc.py`` with multiplication:

.. code-block:: python

   "Simple calculator"
   import argparse
   import argparse_action

   parser = argparse.ArgumentParser(description=__doc__)
   action = argparse_action.Action(parser)

   @action.add()
   def add(a: int, b: int):
       "Add two numberss together"
       print(a + b)

   @action.add()
   def mul(a: int, b: int):
       "Multiply two numbers"
       print(a * b)

   namespace = parser.parse_args()
   namespace.action(namespace)


The ``argparse_action.Action`` is used here to register a subparser for the functions.
So the usage help will differ a bit:

.. code-block::

   $ python3 calc.py -h
   usage: calc.py [-h] command ...

   Simple calculator

   positional arguments:
     command
       add       Add two numbers together
       mul       Multiply two numbers

   optional arguments:
     -h, --help  show this help message and exit

.. code-block::

   $ python3 calc.py mul -h
   usage: calc.py mul [-h] a b

   positional arguments:
     a
     b

   optional arguments:
     -h, --help  show this help message and exit

It works as it expected:

.. code-block::

   $ python3 calc.py mul 12 2
   24

Command aliases
---------------

It's tedious to type so much: ``add``, ``mul``. How about some command aliases:

.. code-block:: python

   @action.add("a", "+")
   def add(a: int, b: int):
       print(a + b)

``action.add()`` registers arbitrary number of aliases from its parameters.

.. code-block::

   $ python3 calc.py + 4 3
   7

CLI options
-----------

We should add some other arithmetics like square:

.. code-block:: python

   @action.add()
   def square(a: int):
       print(a ** at)

.. code-block::

   $ python3 calc.py square 3
   9

It's dull. How about a more generic option:

.. code-block:: python

   @action.add()
   def pow(a: int, at: int = 2):
       print(a ** at)

``argparse_action`` will create cli options from default values:

.. code-block::

   $ python3 calc.py pow 3
   9

   $ python3 calc.py pow 3 --at 3
   27

That's it.
