:orphan:

:mod:`cloup._util`
==================

.. py:module:: cloup._util

.. autoapi-nested-parse::

   Generic utilities.





                              


Functions Summary
-----------------

.. autosummary::

   cloup._util.class_name
   cloup._util.check_arg
   cloup._util.indent_lines
   cloup._util.make_repr
   cloup._util.make_one_line_repr
   cloup._util.pluralize


                                           
Contents
--------
.. function:: class_name(obj)


.. function:: check_arg(condition: bool, msg: str = '')


.. function:: indent_lines(lines: Iterable[str], width=2) -> List[str]


.. function:: make_repr(obj, *args, _line_len: int = 60, _indent: int = 2, **kwargs) -> str

   Generate repr(obj).

   :param obj:
       object to represent
   :param args:
       positional arguments in the repr
   :param _line_len:
       if the repr length exceeds this, arguments will be on their own line;
       if negative, the repr will be in a single line regardless of its length
   :param _indent:
       indentation width of arguments in case they are shown in their own line
   :param kwargs:
       keyword arguments in the repr
   :return: str


.. function:: make_one_line_repr(obj, *args, **kwargs)


.. function:: pluralize(count: int, zero: str = '', one: str = '', many: str = '') -> str



                                         