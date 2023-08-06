
:mod:`cloup`
============

.. py:module:: cloup

.. autoapi-nested-parse::

   Top-level package for cloup.


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   constraints/index.rst



                              

Classes summary
---------------

.. autosummary::

   cloup.GroupedOption
   cloup.OptionGroup
   cloup.OptionGroupMixin
   cloup.Section
   cloup.GroupSection
   cloup.SectionMixin
   cloup.Command
   cloup.Group
   cloup.MultiCommand
   cloup.ConstraintMixin

Functions Summary
-----------------

.. autosummary::

   cloup.option
   cloup.option_group
   cloup.command
   cloup.group
   cloup.constraint


                                           
Contents
--------
.. data:: __author__
   :annotation: = Gianluca Gippetto

   

.. data:: __email__
   :annotation: = gianluca.gippetto@gmail.com

   

.. data:: __version__
   :annotation: = 0.4.2

   

.. py:class:: GroupedOption(*args, group: Optional[OptionGroup] = None, **attrs)

   Bases: :class:`click.Option`

   A click.Option with an extra field ``group`` of type OptionGroup 


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


.. py:class:: Section(title: str, commands: Subcommands = (), sorted: bool = False)

   A group of (sub)commands to show in the same help section of a
   ``MultiCommand``. You can use sections with any `Command` that inherits
   from :class:`SectionMixin`.

   .. versionchanged:: 0.5.0
       This class was renamed from ``GroupSection`` (deprecated) to ``Section``.

   .. method:: sorted(cls, title: str, commands: Subcommands = ()) -> 'Section'
      :classmethod:


   .. method:: add_command(self, cmd: click.Command, name: Optional[str] = None)


   .. method:: list_commands(self) -> List[Tuple[str, click.Command]]


   .. method:: __len__(self) -> int


   .. method:: __repr__(self) -> str

      Return repr(self).



.. py:class:: GroupSection(*args, **kwargs)

   Bases: :class:`cloup._sections.Section`

   Old name of `Section` when the implementation of the feature was
   hard-coded and tightly coupled to ``cloup.Group``.

   .. deprecated:: 0.5.0
       To be removed in v0.6.0. Use ``Section`` instead.


.. py:class:: SectionMixin(*args, commands: Optional[Dict[str, click.Command]] = None, sections: Iterable[Section] = (), align_sections: bool = True, **kwargs)

   Adds to a click.MultiCommand the possibility to organize its subcommands
   in multiple help sections.

   Sections can be specified in the following ways:

   #. passing a list of :class:`Section` objects to the constructor setting
      the argument ``sections``
   #. using :meth:`add_section` to add a single section
   #. using :meth:`add_command` with the argument `section` set

   Commands not assigned to any user-defined section are added to the
   "default section", whose title is "Commands" or "Other commands" depending
   on whether it is the only section or not. The default section is the last
   shown section in the help and its commands are listed in lexicographic order.

   .. versionadded:: 0.5.0

   .. method:: add_section(self, section: Section)

      Adds a :class:`Section` to this group. You can add the same
      section object a single time. 


   .. method:: section(self, title: str, *commands: click.Command, **attrs) -> Section

      Creates a new :class:`Section`, adds it to this group and returns it. 


   .. method:: add_command(self, cmd: click.Command, name: Optional[str] = None, section: Optional[Section] = None)

      Adds a new command. If ``section`` is None, the command is added to the default section.


   .. method:: list_sections(self, ctx: click.Context, include_default_section: bool = True) -> List[Section]

      Returns the list of all sections in the "correct order".
      if ``include_default_section=True`` and the default section is non-empty,
      it will be included at the end of the list. 


   .. method:: format_commands(self, ctx: click.Context, formatter: click.HelpFormatter)


   .. method:: format_section(self, ctx: click.Context, formatter: click.HelpFormatter, section: Section, command_col_width: Optional[int] = None)



.. py:class:: Command(*args, **kwargs)

   Bases: :class:`cloup.constraints.ConstraintMixin`, :class:`cloup._option_groups.OptionGroupMixin`, :class:`click.Command`

   A ``click.Command`` supporting option groups.
   This class is obtained by mixing :class:`click.Command` with
   :class:`cloup.OptionGroupMixin`.


.. py:class:: Group(name: Optional[str] = None, commands: Optional[Dict[str, click.Command]] = None, sections: Iterable[Section] = (), align_sections: bool = True, **attrs)

   Bases: :class:`cloup._sections.SectionMixin`, :class:`click.Group`

   A ``click.Group`` that allows to organize its subcommands in multiple help
   sections and and whose subcommands are, by default, of type
   :class:`cloup.Command`.

   This class is just a :class:`click.Group` mixed with :class:`SectionMixin`
   that overrides the decorators :meth:`command` and :meth:`group` so that
   a ``section`` for the created subcommand can be specified.

   See the docstring of the two superclasses for more details.

   .. method:: command(self, name: Optional[str] = None, section: Optional[Section] = None, cls: Optional[Type[click.Command]] = None, **attrs)

      Creates a new command and adds it to this group.


   .. method:: group(self, name: Optional[str] = None, section: Optional[Section] = None, cls: Optional[Type[click.Group]] = None, **attrs)

      A shortcut decorator for declaring and attaching a group to
      the group.  This takes the same arguments as :func:`group` but
      immediately registers the created command with this instance by
      calling into :meth:`add_command`.



.. py:class:: MultiCommand(*args, **kwargs)

   Bases: :class:`cloup._sections.SectionMixin`, :class:`click.MultiCommand`

   A ``click.MultiCommand`` that allows to organize its subcommands in
   multiple help sections and and whose subcommands are, by default, of type
   :class:`cloup.Command`.

   This class is just a :class:`click.MultiCommand` mixed with
   :class:`SectionMixin`. See the docstring of the two superclasses for more
   details.


.. function:: command(name: Optional[str] = None, cls: Type[click.Command] = Command, **attrs)

   Decorator that creates a new command using the wrapped function as callback.

   The only differences with respect to ``click.commands`` are:

   - this decorator creates a ``cloup.Command`` by default;
   - this decorator supports ``@constraint``.

   :param name: name of the command
   :param cls: type of click.Command
   :param attrs: any argument you can pass to :func:`click.command`


.. function:: group(name: Optional[str] = None, cls: Type[click.Group] = Group, **attrs)

   Creates a new :class:`Group` using the decorated function as
   callback. This is just a convenience function equivalent to::

       click.group(name, cls=cloup.Group, **attrs)

   :param name: name of the command
   :param cls: type of Group
   :param attrs: any argument you can pass to :func:`click.group`


.. py:class:: ConstraintMixin(*args, constraints: Sequence[BoundConstraintSpec] = (), show_constraints: bool = False, **kwargs)

   Provides support to constraints.

   .. method:: parse_args(self, ctx, args)


   .. method:: get_param_by_name(self, name: str) -> Parameter


   .. method:: get_params_by_name(self, names: Iterable[str]) -> List[Parameter]


   .. method:: format_constraints(self, ctx, formatter) -> None


   .. method:: format_help(self, ctx, formatter: HelpFormatter) -> None



.. function:: constraint(constr: Constraint, params: Iterable[str])

   Registers a constraint.



                                         