Tutorial
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The tutorial assumes that the example snippets are saved as ``main.py``.



inject argpasre argument options
--------------------------------


.. literalinclude:: /examples/inject_argument_options/main.py
  :language: python

.. literalinclude:: /examples/inject_argument_options/help

.. literalinclude:: /examples/inject_argument_options/call

Short option can be defined with single character function argument
-------------------------------------------------------------------


.. literalinclude:: /examples/short_option/main.py
  :language: python

.. literalinclude:: /examples/short_option/call

Register command alias
----------------------


.. literalinclude:: /examples/register_command_alias/main.py
  :language: python

.. literalinclude:: /examples/register_command_alias/cmd_p

.. literalinclude:: /examples/register_command_alias/cmd_print

.. literalinclude:: /examples/register_command_alias/cmd_echo

Expose single function
----------------------


.. literalinclude:: /examples/expose_single_function/main.py
  :language: python

.. literalinclude:: /examples/expose_single_function/help

.. literalinclude:: /examples/expose_single_function/call

Expose multiple functions as commands
-------------------------------------


.. literalinclude:: /examples/expose_multiple_functions_as_commands/cmd_oche

.. literalinclude:: /examples/expose_multiple_functions_as_commands/main.py
  :language: python

.. literalinclude:: /examples/expose_multiple_functions_as_commands/help

.. literalinclude:: /examples/expose_multiple_functions_as_commands/cmd_echo

CLI option flag from boolean default value
------------------------------------------


.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call_upper

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/main.py
  :language: python

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call

varg parameter is handled as nargs=* argument
---------------------------------------------


.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/main.py
  :language: python

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/call_spam

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/help

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/call

CLI option from default value
-----------------------------


.. literalinclude:: /examples/cli_option_from_default_value/main.py
  :language: python

.. literalinclude:: /examples/cli_option_from_default_value/call_sam

.. literalinclude:: /examples/cli_option_from_default_value/call

Enum annotation register argument choices
-----------------------------------------


.. literalinclude:: /examples/enum_choices/main.py
  :language: python

.. literalinclude:: /examples/enum_choices/help

.. literalinclude:: /examples/enum_choices/call_default

.. literalinclude:: /examples/enum_choices/call
