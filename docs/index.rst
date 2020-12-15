.. argparse_action documentation master file, created by
   sphinx-quickstart on Mon Dec 14 23:29:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to argparse_action's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Concept
-------

``argparse_action`` aims to be a minimalistic extension of ``argparse`` and creates
cli options from the function signature given by ``inspect.signature``.


Example
.......

.. code-block:: python

   import argparse
   import argparse_action

   parser = argparse.ArgumentParser()
   action = argparse_action.Action(parser)

   @action.add("e")
   def echo(word, upper=False):
       print(word.upper() if upper else word)

   namespace = pasrer.parse_args()
   namespace.action(namespace)

Asumes that the code above is saved as ``my_script.py``:

.. code-block::

   $ python3 my_script.py echo hello
   hello

   $ python3 my_script.py e hello
   hello

   $ python3 my_script.py echo --upper hello
   HELLO


Installation
------------

.. code-block::

   pip install argparse_action

Development
-----------

``argparse_action`` development is managed on github_.

.. _github: https://github.com/nyirog/argparse_action

Articles
--------

.. toctree::
   :maxdepth: 2

   articles/getting_started
   articles/tutorial

API reference
-------------

.. toctree::
   :maxdepth: 2

   api/argparse_action



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
