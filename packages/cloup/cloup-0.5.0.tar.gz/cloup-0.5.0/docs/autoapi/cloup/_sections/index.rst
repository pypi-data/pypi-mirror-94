:orphan:

:mod:`cloup._sections`
======================

.. py:module:: cloup._sections





                              

Classes summary
---------------

.. autosummary::

   cloup._sections.Section
   cloup._sections.GroupSection
   cloup._sections.SectionMixin



                                           
Contents
--------
.. data:: CommandType
   

   

.. data:: Subcommands
   

   

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




                                         