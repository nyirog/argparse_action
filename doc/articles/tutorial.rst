Tutorial
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The tutorial assumes that the example snippets are saved as ``my_script.py``.

Expose single function
----------------------

.. code-block:: python

   "Example script for argparse_action"
   import argparse
   import argparse_action

   def echo(word):
       print(word)

   parser = argparse.ArgumentParser(description=__doc__)
   argparse_action.add_action(parser, echo)
   namespace = parser.parse_args()
   namespace.action(namespace)

.. code-block::

   $ python3 my_script.py -h
   usage: my_script.py [-h] word

   Example script for argparse_action

   positional arguments:
     word

   optional arguments:
     -h, --help  show this help message and exit

   $ python3 echo.py hello
   hello

Expose multiple functions as commands
-------------------------------------

.. code-block:: python

   "Example script for argparse_action"
   import argparse
   import argparse_action

   parser = argparse.ArgumentParser(description=__doc__)
   action = argparse_action.Action(parser)

   @action.add()
   def echo(parameter):
       "echo the cli argument"
       print(parameter)

   @action.add()
   def oche(parameter):
       "echo the revered cli argrument"
       acc = list(parameter)
       acc.reverse()
       print("".join(acc))

   namespace = parser.parse_args()
   namespace.action(namespace)

.. code-block::

   $ python3 my_script.py  -h
   usage: my_script.py [-h] command ...

   Example script for argparse_action

   positional arguments:
     command
       echo  echo the cli argument
       oche  echo the revered cli argument

   optional arguments:
     -h, --help  show this help message and exit

   $ python3 my_script.py echo hello
   hello

   $ python3 my_script.py oche hello
   olleh


Register command alias
----------------------

.. code-block:: python

   @action.add("print", "p")
   def echo(parameter):
       "echo the cli argument"
       print(parameter)

.. code-block::

   $ python3 my_script.py echo hello
   hello

   $ python3 my_script.py print bello
   bello

   $ python3 my_script.py p hello-bello
   hello-bello

CLI option from default value
-----------------------------

.. code-block:: python

   @action.add()
   def echo(word, name="joe"):
       print(f"{word} {name}")

.. code-block::

   $ python3 my_script.py echo hello
   hello joe

   $ python3 my_script.py echo hello --name sam
   hello sam

CLI option flaf from boolean default value
------------------------------------------

.. code-block:: python

   @action.add()
   def echo(word, upper=False):
       print(word.upper() if upper else word)

.. code-block::

   $ python3 my_script.py echo hello
   hello

   $ python3 my_script.py echo hello --upper
   HELLO
