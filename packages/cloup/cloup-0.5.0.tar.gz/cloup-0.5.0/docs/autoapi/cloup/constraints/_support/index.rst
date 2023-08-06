:orphan:

:mod:`cloup.constraints._support`
=================================

.. py:module:: cloup.constraints._support





                              

Classes summary
---------------

.. autosummary::

   cloup.constraints._support.BoundConstraintSpec
   cloup.constraints._support.BoundConstraint
   cloup.constraints._support.ConstraintMixin

Functions Summary
-----------------

.. autosummary::

   cloup.constraints._support.constraint


                                           
Contents
--------
.. py:class:: BoundConstraintSpec

   Bases: :class:`typing.NamedTuple`

   Typed version of namedtuple.

   Usage in Python versions >= 3.6::

       class Employee(NamedTuple):
           name: str
           id: int

   This is equivalent to::

       Employee = collections.namedtuple('Employee', ['name', 'id'])

   The resulting class has an extra __annotations__ attribute, giving a
   dict that maps field names to types.  (The field names are also in
   the _fields attribute, which is part of the namedtuple API.)
   Alternative equivalent keyword syntax is also accepted::

       Employee = NamedTuple('Employee', name=str, id=int)

   In Python versions <= 3.5 use::

       Employee = NamedTuple('Employee', [('name', str), ('id', int)])

   .. attribute:: constraint
      :annotation: :Constraint

      

   .. attribute:: params
      :annotation: :Sequence[str]

      


.. function:: constraint(constr: Constraint, params: Iterable[str])

   Registers a constraint.


.. py:class:: BoundConstraint

   Bases: :class:`typing.NamedTuple`

   Typed version of namedtuple.

   Usage in Python versions >= 3.6::

       class Employee(NamedTuple):
           name: str
           id: int

   This is equivalent to::

       Employee = collections.namedtuple('Employee', ['name', 'id'])

   The resulting class has an extra __annotations__ attribute, giving a
   dict that maps field names to types.  (The field names are also in
   the _fields attribute, which is part of the namedtuple API.)
   Alternative equivalent keyword syntax is also accepted::

       Employee = NamedTuple('Employee', name=str, id=int)

   In Python versions <= 3.5 use::

       Employee = NamedTuple('Employee', [('name', str), ('id', int)])

   .. attribute:: constraint
      :annotation: :Constraint

      

   .. attribute:: params
      :annotation: :Sequence[Parameter]

      

   .. method:: check_consistency(self)


   .. method:: check_values(self, ctx: Context)


   .. method:: get_help_record(self, ctx: Context) -> Optional[Tuple[str, str]]



.. py:class:: ConstraintMixin(*args, constraints: Sequence[BoundConstraintSpec] = (), show_constraints: bool = False, **kwargs)

   Provides support to constraints.

   .. method:: parse_args(self, ctx, args)


   .. method:: get_param_by_name(self, name: str) -> Parameter


   .. method:: get_params_by_name(self, names: Iterable[str]) -> List[Parameter]


   .. method:: format_constraints(self, ctx, formatter) -> None


   .. method:: format_help(self, ctx, formatter: HelpFormatter) -> None




                                         