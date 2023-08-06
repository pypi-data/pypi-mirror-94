:orphan:

:mod:`cloup.constraints._core`
==============================

.. py:module:: cloup.constraints._core





                              

Classes summary
---------------

.. autosummary::

   cloup.constraints._core.Constraint
   cloup.constraints._core.Operator
   cloup.constraints._core.And
   cloup.constraints._core.Or
   cloup.constraints._core.Rephraser
   cloup.constraints._core.WrapperConstraint
   cloup.constraints._core.RequireAtLeast
   cloup.constraints._core.AcceptAtMost
   cloup.constraints._core.RequireExactly
   cloup.constraints._core.AcceptBetween



                                           
Contents
--------
.. data:: Op
   

   

.. data:: HelpRephraser
   

   

.. data:: ErrorRephraser
   

   

.. py:class:: Constraint

   Bases: :class:`abc.ABC`

   A constraint that can be checked against an arbitrary collection of CLI
   parameters with respect to a specific :class:`click.Context` (which
   contains the values assigned to the parameters in ``ctx.params``).

   .. method:: must_check_consistency(cls) -> bool
      :classmethod:

      Returns True if consistency checks are enabled.


   .. method:: toggle_consistency_checks(cls, value: bool)
      :classmethod:

      Enables/disables consistency checks. Enabling means that:

      - :meth:`check` will call :meth:`check_consistency`
      - :class:`~cloup.ConstraintMixin` will call `check_consistency` on
        constraints it is responsible for before parsing CLI arguments.


   .. method:: consistency_checks_toggled(cls, value: bool)
      :classmethod:


   .. method:: help(self, ctx: Context) -> str
      :abstractmethod:

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
      :abstractmethod:

      Checks that the constraint is satisfied by the input parameters in the
      given context, which (among other things) contains the values assigned
      to the parameters in ``ctx.params``.

      You probably don't want to call this method directly.
      Use :meth:`check` instead.

      :param params: list of :class:`click.Parameter` instances
      :param ctx: :class:`click.Context`
      :raises:
          :exc:`~cloup.constraints.ConstraintViolated`


   .. method:: check(self, params: Sequence[Parameter], ctx: Optional[Context] = None) -> None
               check(self, params: Iterable[str], ctx: Optional[Context] = None) -> None

      Raises an exception if the constraint is not satisfied by the input
      parameters in the given (or current) context.

      This method calls both :meth:`check_consistency` (if enabled) and
      :meth:`check_values`.

      .. tip::
          By default :meth:`check_consistency` is called since it shouldn't
          have any performance impact. Nonetheless, you can disable it in
          production passing ``False`` to :meth:`toggle_consistency_checks`.

      :param params: an iterable of parameter names or a sequence of
                     :class:`click.Parameter`
      :param ctx: a `Context`; if not provided, :func:`click.get_current_context`
                  is used
      :raises:
          :exc:`~cloup.constraints.ConstraintViolated`
          :exc:`~cloup.constraints.UnsatisfiableConstraint`


   .. method:: rephrased(self, help: Union[None, str, HelpRephraser] = None, error: Union[None, str, ErrorRephraser] = None) -> 'Rephraser'


   .. method:: hidden(self) -> 'Rephraser'

      Hides this constraint from the command help.


   .. method:: __call__(self, param_names: Iterable[str], ctx: Optional[Context] = None) -> None


   .. method:: __or__(self, other: Constraint) -> 'Or'


   .. method:: __and__(self, other: Constraint) -> 'And'


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: Operator(*constraints: Constraint)

   Bases: :class:`cloup.constraints._core.Constraint`, :class:`abc.ABC`

   Base class for all n-ary operators defined on constraints. 

   .. attribute:: HELP_SEP
      :annotation: :str

      

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


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: And(*constraints: Constraint)

   Bases: :class:`cloup.constraints._core.Operator`

   It's satisfied if all operands are satisfied.

   .. attribute:: HELP_SEP
      :annotation: =  and 

      

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


   .. method:: __and__(self, other) -> 'And'



.. py:class:: Or(*constraints: Constraint)

   Bases: :class:`cloup.constraints._core.Operator`

   It's satisfied if at least one of the operands is satisfied.

   .. attribute:: HELP_SEP
      :annotation: =  or 

      

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


   .. method:: __or__(self, other) -> 'Or'



.. py:class:: Rephraser(constraint: Constraint, help: Union[None, str, HelpRephraser] = None, error: Union[None, str, ErrorRephraser] = None)

   Bases: :class:`cloup.constraints._core.Constraint`

   A Constraint decorator that can override the help and/or the error
   message of the wrapped constraint.

   This is useful also for defining new constraints.
   See also :class:`WrapperConstraint`.

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


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: WrapperConstraint(constraint: Constraint, **attrs)

   Bases: :class:`cloup.constraints._core.Constraint`

   Abstract class that wraps another constraint and delegates all methods
   to it. Useful when you want to define a parametric constraint combining
   other existing constraints minimizing the boilerplate.

   This is an alternative to defining a function and using :class:`Rephraser`.
   Feel free to do that in your code, but cloup will stick to the convention
   that parametric constraints are defined as classes and written in
   camel-case.

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


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: RequireAtLeast(n: int)

   Bases: :class:`cloup.constraints._core.Constraint`

   Satisfied if the number of set parameters is >= n.

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


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: AcceptAtMost(n: int)

   Bases: :class:`cloup.constraints._core.Constraint`

   Satisfied if the number of set parameters is <= n.

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


   .. method:: __repr__(self)

      Return repr(self).



.. py:class:: RequireExactly(n: int)

   Bases: :class:`cloup.constraints._core.WrapperConstraint`

   Requires an exact number of parameters to be set.

   .. method:: help(self, ctx: Context) -> str

      A description of the constraint. 


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



.. py:class:: AcceptBetween(min: int, max: int)

   Bases: :class:`cloup.constraints._core.WrapperConstraint`

   Abstract class that wraps another constraint and delegates all methods
   to it. Useful when you want to define a parametric constraint combining
   other existing constraints minimizing the boilerplate.

   This is an alternative to defining a function and using :class:`Rephraser`.
   Feel free to do that in your code, but cloup will stick to the convention
   that parametric constraints are defined as classes and written in
   camel-case.

   .. method:: help(self, ctx: Context) -> str

      A description of the constraint. 



.. data:: require_all
   

   

.. data:: accept_none
   

   

.. data:: all_or_none
   

   

.. data:: mutually_exclusive
   

   


                                         