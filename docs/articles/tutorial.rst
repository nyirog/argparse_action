Tutorial
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The tutorial assumes that the example snippets are saved as ``main.py``.



Expose single function
----------------------


.. literalinclude:: /examples/expose_single_function/call

.. literalinclude:: /examples/expose_single_function/main.py
  :language: python

.. literalinclude:: /examples/expose_single_function/help

Expose multiple functions as commands
-------------------------------------


.. literalinclude:: /examples/expose_multiple_functions_as_commands/cmd_echo

.. literalinclude:: /examples/expose_multiple_functions_as_commands/main.py
  :language: python

.. literalinclude:: /examples/expose_multiple_functions_as_commands/help

.. literalinclude:: /examples/expose_multiple_functions_as_commands/cmd_oche

Arbitrary argument is handled as nargs=* argument
-------------------------------------------------


.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/call

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/main.py
  :language: python

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/help

.. literalinclude:: /examples/varg_parameter_is_handled_as_nargs_argument/call_spam

Short option can be defined with single character function argument
-------------------------------------------------------------------


.. literalinclude:: /examples/short_option/call

.. literalinclude:: /examples/short_option/main.py
  :language: python

Extra argpasre options can be injected
--------------------------------------


.. literalinclude:: /examples/inject_argument_options/call

.. literalinclude:: /examples/inject_argument_options/main.py
  :language: python

.. literalinclude:: /examples/inject_argument_options/help

Argparse 'append' action can be forced with sequence default value
------------------------------------------------------------------


.. literalinclude:: /examples/append_cli_options/call

.. literalinclude:: /examples/append_cli_options/main.py
  :language: python

Initiate python logging with argparse_action
--------------------------------------------


.. literalinclude:: /examples/logging/call

.. literalinclude:: /examples/logging/main.py
  :language: python

.. literalinclude:: /examples/logging/help

.. literalinclude:: /examples/logging/call-on-info

Arbitrary argument can be annoted
---------------------------------


.. literalinclude:: /examples/varg_can_be_annotated/call

.. literalinclude:: /examples/varg_can_be_annotated/main.py
  :language: python

Register command alias
----------------------


.. literalinclude:: /examples/register_command_alias/cmd_echo

.. literalinclude:: /examples/register_command_alias/cmd_print

.. literalinclude:: /examples/register_command_alias/main.py
  :language: python

.. literalinclude:: /examples/register_command_alias/cmd_p

Enum annotation register argument choices
-----------------------------------------


.. literalinclude:: /examples/enum_choices/call

.. literalinclude:: /examples/enum_choices/main.py
  :language: python

.. literalinclude:: /examples/enum_choices/help

.. literalinclude:: /examples/enum_choices/call_default

CLI option from default value
-----------------------------


.. literalinclude:: /examples/cli_option_from_default_value/call

.. literalinclude:: /examples/cli_option_from_default_value/main.py
  :language: python

.. literalinclude:: /examples/cli_option_from_default_value/call_sam

.. literalinclude:: /examples/cli_option_from_default_value/help

CLI option flag from boolean default value
------------------------------------------


.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/main.py
  :language: python

.. literalinclude:: /examples/cli_option_flag_from_bool_default_value/call_upper
