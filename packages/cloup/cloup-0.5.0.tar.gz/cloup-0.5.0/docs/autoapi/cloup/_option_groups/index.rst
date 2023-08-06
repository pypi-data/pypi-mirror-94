:orphan:

:mod:`cloup._option_groups`
===========================

.. py:module:: cloup._option_groups

.. autoapi-nested-parse::

   Implements support to option group.





                              

Classes summary
---------------

.. autosummary::

   cloup._option_groups.OptionGroup
   cloup._option_groups.GroupedOption
   cloup._option_groups.OptionGroupMixin

Functions Summary
-----------------

.. autosummary::

   cloup._option_groups.has_option_group
   cloup._option_groups.get_option_group_of
   cloup._option_groups.option
   cloup._option_groups.option_group


                                           
Contents
--------
.. data:: C
   

   

.. data:: OptionDecorator
   

   

.. data:: OptionGroupDecorator
   

   

.. py:class:: OptionGroup(name: str, help: Optional[str] = None, constraint: Optional[Constraint] = None)

   .. method:: get_help_records(self, ctx: click.Context)


   .. method:: option(self, *param_decls, **attrs)


   .. method:: __iter__(self)


   .. method:: __getitem__(self, i: int) -> click.Option


   .. method:: __len__(self) -> int


   .. method:: __repr__(self) -> str

      Return repr(self).


   .. method:: __str__(self) -> str

      Return str(self).



.. py:class:: GroupedOption(*args, group: Optional[OptionGroup] = None, **attrs)

   Bases: :class:`click.Option`

   A click.Option with an extra field ``group`` of type OptionGroup 


.. function:: has_option_group(param) -> bool


.. function:: get_option_group_of(param, default=None)


.. py:class:: OptionGroupMixin(*args, align_option_groups: bool = True, **kwargs)

   Implements support to option groups.

   .. versionadded:: 0.5.0

   .. important::
       In order to check the constraints defined on the option groups,
       a command must inherits from :class:`cloup.ConstraintMixin` too!

   .. method:: get_ungrouped_options(self, ctx: click.Context) -> Sequence[click.Option]


   .. method:: get_option_group_title(self, ctx: click.Context, opt_group: OptionGroup) -> str


   .. method:: format_option_group(self, ctx: click.Context, formatter: click.HelpFormatter, opt_group: OptionGroup, help_records: Optional[Sequence] = None)


   .. method:: format_options(self, ctx: click.Context, formatter: click.HelpFormatter, max_option_width: int = 30)



.. function:: option(*param_decls, group: Optional[OptionGroup] = None, cls: Type[click.Option] = GroupedOption, **attrs) -> OptionDecorator


.. function:: option_group(name: str, help: str, *options: OptionDecorator, constraint: Optional[Constraint] = None) -> OptionGroupDecorator
              option_group(name: str, *options: OptionDecorator, help: Optional[str] = None, constraint: Optional[Constraint] = None) -> OptionGroupDecorator

   Attaches an option group to the command. This decorator is overloaded with
   two signatures::

       @option_group(name: str, *options, help: Optional[str] = None)
       @option_group(name: str, help: str, *options)

   In other words, if the second position argument is a string, it is interpreted
   as the "help" argument. Otherwise, it is interpreted as the first option;
   in this case, you can still pass the help as keyword argument.

   :param name: a mandatory name/title for the group
   :param help: an optional help string for the group
   :param options: option decorators like `click.option`
   :param constraint: a ``Constraint`` to validate on this option group
   :return: a decorator that attaches the contained options to the decorated
            function



                                         