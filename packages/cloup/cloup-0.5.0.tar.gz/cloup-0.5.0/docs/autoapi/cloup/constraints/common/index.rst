
:mod:`cloup.constraints.common`
===============================

.. py:module:: cloup.constraints.common

.. autoapi-nested-parse::

   Useful functions used for implementing constraints and predicates.





                              


Functions Summary
-----------------

.. autosummary::

   cloup.constraints.common.param_value_is_set
   cloup.constraints.common.get_params_whose_value_is_set
   cloup.constraints.common.get_required_params
   cloup.constraints.common.get_param_label
   cloup.constraints.common.join_param_labels
   cloup.constraints.common.param_label_by_name
   cloup.constraints.common.param_value_by_name


                                           
Contents
--------
.. function:: param_value_is_set(param: Parameter, value: Any) -> bool

   Defines what it means for a parameter of a specific kind to be "set".

   All cases are obvious besides that of boolean options:
   - (common rule) if the value is ``None``, the parameter is unset;
   - a parameter that takes multiple values is set if at least one argument is provided;
   - a boolean **flag** is set only if True;
   - a boolean option is set if not None, even if it's False.


.. function:: get_params_whose_value_is_set(params: Iterable[Parameter], values: Dict[str, Any]) -> List[Parameter]

   Filters ``params`` returning only the parameters that have a value.
   Boolean flags are considered "set" if their value is ``True``.


.. function:: get_required_params(params: Iterable[Parameter]) -> List[Parameter]


.. function:: get_param_label(param: Parameter) -> str


.. function:: join_param_labels(params: Iterable[Parameter], sep: str = ', ') -> str


.. function:: param_label_by_name(ctx, name: str) -> str


.. function:: param_value_by_name(ctx: Context, name: str) -> Any



                                         