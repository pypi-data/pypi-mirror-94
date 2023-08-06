
:mod:`cloup.constraints.exceptions`
===================================

.. py:module:: cloup.constraints.exceptions





                              


Functions Summary
-----------------

.. autosummary::

   cloup.constraints.exceptions.default_constraint_error


                                           
Contents
--------
.. function:: default_constraint_error(params: Iterable[Parameter], desc: str) -> str


.. py:exception:: ConstraintViolated(message: str, ctx: Optional[Context] = None)

   Bases: :class:`click.UsageError`

   An internal exception that signals a usage error.  This typically
   aborts any further handling.

   :param message: the error message to display.
   :param ctx: optionally the context that caused this error.  Click will
               fill in the context automatically in some situations.

   .. method:: default(cls, params: Iterable[Parameter], desc: str, ctx: Optional[Context] = None) -> 'ConstraintViolated'
      :classmethod:



.. py:exception:: UnsatisfiableConstraint(constraint: Constraint, params: Iterable[Parameter], reason: str)

   Bases: :class:`Exception`

   Raised if a constraint cannot be satisfied by a group of parameters
   independently from their values at runtime; e.g. mutually_exclusive cannot
   be satisfied if multiple of the parameters are required. 



                                         