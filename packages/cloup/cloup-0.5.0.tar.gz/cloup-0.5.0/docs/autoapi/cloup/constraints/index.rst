
:mod:`cloup.constraints`
========================

.. py:module:: cloup.constraints

.. autoapi-nested-parse::

   Constraints for parameter groups.

   .. versionadded: v0.5.0



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   common/index.rst
   conditions/index.rst
   exceptions/index.rst


                              

Classes summary
---------------

.. autosummary::

   cloup.constraints.If
   cloup.constraints.AcceptAtMost
   cloup.constraints.AcceptBetween
   cloup.constraints.And
   cloup.constraints.Constraint
   cloup.constraints.Operator
   cloup.constraints.Or
   cloup.constraints.Rephraser
   cloup.constraints.RequireAtLeast
   cloup.constraints.RequireExactly
   cloup.constraints.WrapperConstraint
   cloup.constraints.ConstraintMixin
   cloup.constraints.Equal
   cloup.constraints.IsSet
   cloup.constraints.Not

Functions Summary
-----------------

.. autosummary::

   cloup.constraints.constraint


                                           
Contents
--------
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



.. data:: accept_none
   

   

.. data:: all_or_none
   

   

.. data:: mutually_exclusive
   

   

.. data:: require_all
   

   

.. py:class:: ConstraintMixin(*args, constraints: Sequence[BoundConstraintSpec] = (), show_constraints: bool = False, **kwargs)

   Provides support to constraints.

   .. method:: parse_args(self, ctx, args)


   .. method:: get_param_by_name(self, name: str) -> Parameter


   .. method:: get_params_by_name(self, names: Iterable[str]) -> List[Parameter]


   .. method:: format_constraints(self, ctx, formatter) -> None


   .. method:: format_help(self, ctx, formatter: HelpFormatter) -> None



.. function:: constraint(constr: Constraint, params: Iterable[str])

   Registers a constraint.


.. py:class:: Equal(param_name: str, value: Any)

   Bases: :class:`cloup.constraints.conditions.Predicate`

   True if the parameter value equals ``value``.

   .. method:: description(self, ctx: Context) -> str

      Succint description of the predicate (alias: `desc`).


   .. method:: negated_description(self, ctx: Context) -> str

      Succint description of the negation of this predicate (alias: `neg_desc`).


   .. method:: __call__(self, ctx: Context) -> bool

      Evaluate the predicate on the given context.



.. py:class:: IsSet(param_name: str)

   Bases: :class:`cloup.constraints.conditions.Predicate`

   A ``Callable`` that takes a ``Context`` and returns a boolean, with an
   associated description. Meant to be used as condition in a conditional
   constraint (see :class:`~cloup.constraints.If`).

   .. method:: description(self, ctx: Context) -> str

      Succint description of the predicate (alias: `desc`).


   .. method:: negated_description(self, ctx: Context) -> str

      Succint description of the negation of this predicate (alias: `neg_desc`).


   .. method:: __call__(self, ctx: Context) -> bool

      Evaluate the predicate on the given context.



.. py:class:: Not(predicate: P)

   Bases: :class:`cloup.constraints.conditions.Predicate`, :class:`Generic[P]`

   A ``Callable`` that takes a ``Context`` and returns a boolean, with an
   associated description. Meant to be used as condition in a conditional
   constraint (see :class:`~cloup.constraints.If`).

   .. method:: description(self, ctx: Context) -> str

      Succint description of the predicate (alias: `desc`).


   .. method:: negated_description(self, ctx: Context) -> str

      Succint description of the negation of this predicate (alias: `neg_desc`).


   .. method:: __call__(self, ctx: Context) -> bool

      Evaluate the predicate on the given context.


   .. method:: __invert__(self) -> P


   .. method:: __repr__(self) -> str

      Return repr(self).



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



                                         