
:mod:`cloup.constraints.conditions`
===================================

.. py:module:: cloup.constraints.conditions

.. autoapi-nested-parse::

   This modules contains described predicates that you can use as conditions of
   conditional constraints (see :class:`cloup.constraints.If`).

   Predicates should be treated as immutable objects, even though immutability
   is not (at the moment) enforced.





                              

Classes summary
---------------

.. autosummary::

   cloup.constraints.conditions.Predicate
   cloup.constraints.conditions.Not
   cloup.constraints.conditions.IsSet
   cloup.constraints.conditions.Equal



                                           
Contents
--------
.. data:: P
   

   

.. py:class:: Predicate

   Bases: :class:`abc.ABC`

   A ``Callable`` that takes a ``Context`` and returns a boolean, with an
   associated description. Meant to be used as condition in a conditional
   constraint (see :class:`~cloup.constraints.If`).

   .. method:: description(self, ctx: Context) -> str
      :abstractmethod:

      Succint description of the predicate (alias: `desc`).


   .. method:: negated_description(self, ctx: Context) -> str

      Succint description of the negation of this predicate (alias: `neg_desc`).


   .. method:: desc(self, ctx: Context) -> str

      Short alias for :meth:`description`.


   .. method:: neg_desc(self, ctx: Context) -> str

      Short alias for :meth:`negated_description`.


   .. method:: negated(self)


   .. method:: __call__(self, ctx: Context) -> bool
      :abstractmethod:

      Evaluate the predicate on the given context.


   .. method:: __invert__(self) -> 'Predicate'


   .. method:: __or__(self, other: Predicate) -> '_Or'


   .. method:: __and__(self, other: Predicate) -> '_And'


   .. method:: __repr__(self)

      Return repr(self).



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



.. py:class:: Equal(param_name: str, value: Any)

   Bases: :class:`cloup.constraints.conditions.Predicate`

   True if the parameter value equals ``value``.

   .. method:: description(self, ctx: Context) -> str

      Succint description of the predicate (alias: `desc`).


   .. method:: negated_description(self, ctx: Context) -> str

      Succint description of the negation of this predicate (alias: `neg_desc`).


   .. method:: __call__(self, ctx: Context) -> bool

      Evaluate the predicate on the given context.




                                         