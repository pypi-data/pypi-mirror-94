:orphan:

:mod:`cloup._commands`
======================

.. py:module:: cloup._commands





                              

Classes summary
---------------

.. autosummary::

   cloup._commands.Command
   cloup._commands.MultiCommand
   cloup._commands.Group

Functions Summary
-----------------

.. autosummary::

   cloup._commands.group
   cloup._commands.command


                                           
Contents
--------
.. py:class:: Command(*args, **kwargs)

   Bases: :class:`cloup.constraints.ConstraintMixin`, :class:`cloup._option_groups.OptionGroupMixin`, :class:`click.Command`

   A ``click.Command`` supporting option groups.
   This class is obtained by mixing :class:`click.Command` with
   :class:`cloup.OptionGroupMixin`.


.. py:class:: MultiCommand(*args, **kwargs)

   Bases: :class:`cloup._sections.SectionMixin`, :class:`click.MultiCommand`

   A ``click.MultiCommand`` that allows to organize its subcommands in
   multiple help sections and and whose subcommands are, by default, of type
   :class:`cloup.Command`.

   This class is just a :class:`click.MultiCommand` mixed with
   :class:`SectionMixin`. See the docstring of the two superclasses for more
   details.


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



.. function:: group(name: Optional[str] = None, cls: Type[click.Group] = Group, **attrs)

   Creates a new :class:`Group` using the decorated function as
   callback. This is just a convenience function equivalent to::

       click.group(name, cls=cloup.Group, **attrs)

   :param name: name of the command
   :param cls: type of Group
   :param attrs: any argument you can pass to :func:`click.group`


.. function:: command(name: Optional[str] = None, cls: Type[click.Command] = Command, **attrs)

   Decorator that creates a new command using the wrapped function as callback.

   The only differences with respect to ``click.commands`` are:

   - this decorator creates a ``cloup.Command`` by default;
   - this decorator supports ``@constraint``.

   :param name: name of the command
   :param cls: type of click.Command
   :param attrs: any argument you can pass to :func:`click.command`



                                         