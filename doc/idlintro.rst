.. FIXME: myrpcgen invocation
.. FIXME: provided they are declared before duplicated
.. FIXME: create calculator.idl file

IDL introduction
================

In this section, we will cover MyRPC IDL syntax and basic myrpcgen
(MyRPC code generator tool) usage with included examples.

Namespace declaration
---------------------

Let's start with a simple calculator example. Because MyRPC generates
code, it needs some guidance which namespace the generated stuff will go
into::

  namespace py CalculatorService

Explanation:

* One *namespace* declaration is needed per target language.
* *py* is the name of target language (in this case it is Python). In
  MyRPC slang it is called generator. For available generators, see FIXME.
* *CalculatorService* is the name of Python package where the
  generated files will go into. Actually, the interpretation of namespace
  is generator dependent. For more information, see FIXME.

Methods
-------

Our first method will calculate the sum of two integers::

  beginmethod sum_2
      in 0 required i32 a
      in 1 required i32 b
      out required i32
  endmethod

Explanation:

* *beginmethod* declares a method called *sum_2*.
* Methods can have zero or more input arguments, which are declared
  with *in* keyword. There are two input arguments: *a* and *b*. Both are
  *required*, meaning that they can't be null. If we allow null values,
  then *optional* keyword can be used instead. *i32* is the data type of
  arguments (32 bit signed integer). Integer numbers right after *in*
  are called field identifiers, or fids. During (de)serialization,
  MyRPC uses fids (*0* and *1*) instead of names (*a* and *b*) to identify input
  arguments. Fids must be unique and be between 0 ... 2\ :sup:`16` - 2.
* Return value is specified by *out*. In method declaration, zero
  or exactly one *out* keyword is allowed. If we don't have *out*,
  the method doesn't return value.

In place of *i32*, we can use any other primitive or user-defined type,
provided they are declared before. For more information on types, see
:ref:`typemapping`.

Lists
-----

To allow variable number of input arguments, We can write generalized
version of the sum method by using list instead of separate *a* and *b*
arguments::

  list IntegerList i32

  beginmethod sum_list
      in 0 required IntegerList inlist
      out required i32
  endmethod

Explanation:

* The *list* keyword is used to define new list type, called *IntegerList*.
* List elements have *i32* data type. Any primitive or user-defined data
  type can be used here, provided they are declared before. Elements in list
  can't be null (MyRPC doesn't support it).
* The newly created type (*IntegerList*) can be referenced later, where data
  type expected.

Enumeration
-----------

FIXME: To be written.

Structure
---------

FIXME: To be written.

Exceptions
----------

FIXME: To be written.::

  beginexception OperationException
      field 0 optional message
  endexception

  beginmethod div
      in 0 required i32 a
      in 1 required i32 b
      out required float
      throw OperationException
  endmethod

Comments
--------

The hash character (*#*) is used to start a comment in MyRPC IDL.
