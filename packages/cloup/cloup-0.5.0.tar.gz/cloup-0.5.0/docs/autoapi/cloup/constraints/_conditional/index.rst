:orphan:

:mod:`cloup.constraints._conditional`
=====================================

.. py:module:: cloup.constraints._conditional

.. autoapi-nested-parse::

   This modules contains classes to create conditional constraints.





                              

Classes summary
---------------

.. autosummary::

   cloup.constraints._conditional.If

Functions Summary
-----------------

.. autosummary::

   cloup.constraints._conditional.as_predicate


                                           
Contents
--------
.. function:: as_predicate(arg: Union[str, Predicate]) -> Predicate


.. py:class:: If(condition: Union[str, Predicate], then: Constraint, else_: Optional[Constraint] = None)

   Bases: :class:`cloup.constraints._core.Constraint`

   A constraint that can be checked against an arbitrary collection of CLI
   parameters with respect to a specific :class:`click.Context` (which
   contains the values assigned to the parameters in ``ctx.params``).

   .. method:: help(self, ctx: Context) -> str

      A description of the constraint. 


   .. method:: check_consistency(self, params: Sequence[Parameter]) -> None

      Performs some sanity checks that detect inconsistencies between this
      constraints and the properties of the input parameters (e.g. required).

      For example, a constraint that requires the parameters to be mutually
      exclusive is not consistent with a group of parameters with multiple
      required options.

      These sanity checks are meant to catch developer's mistakes and don't
      depend on the values assigned to the parameters; therefore:

      - they can be performed before any parameter parsing
      - they can be disabled in production (see :meth:`toggle_consistency_checks`)

      :param params: list of :class:`click.Parameter` instances
      :raises: :exc:`~cloup.constraints.errors.UnsatisfiableConstraint`
               if the constraint cannot be satisfied independently from the values
               provided by the user


   .. method:: check_values(self, params: Sequence[Parameter], ctx: Context)

      Checks that the constraint is satisfied by the input parameters in the
      given context, which (among other things) contains the values assigned
      to the parameters in ``ctx.params``.

      You probably don't want to call this method directly.
      Use :meth:`check` instead.

      :param params: list of :class:`click.Parameter` instances
      :param ctx: :class:`click.Context`
      :raises:
          :exc:`~cloup.constraints.ConstraintViolated`


   .. method:: __repr__(self) -> str

      Return repr(self).




                                         