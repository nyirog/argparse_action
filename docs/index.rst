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

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/main.py
  :language: python

Asumes that the code above is saved as ``main.py``:

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call_upper

Installation
------------

.. code-block::

   pip install argparse_action

Articles
--------

.. toctree::
   :maxdepth: 2

   articles/getting_started
   articles/tutorial
   articles/development

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
