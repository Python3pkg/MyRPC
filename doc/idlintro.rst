.. FIXME: provided they are declared before duplicated
.. FIXME: create calculator.idl file
.. FIXME: or any user-defined types: but not exceptions
.. FIXME: check examples for syntax/myrpcgen invocation
.. FIXME: check&read
.. FIXME: s
.. FIXME: client/processor terminology cleanup

IDL introduction
================

In this section, we will cover MyRPC IDL syntax and basic myrpcgen
(MyRPC code generator tool) usage with included examples.

.. _idlintro-namespace:

Namespace
---------

Let's start with a simple calculator example. Because MyRPC generates
code, it needs some guidance which namespace the generated stuff will go
into::

  namespace py CalculatorService

Explanation:

* One *namespace* declaration is needed per target language we would like
  to generate code for.
* *py* is the name of target language (in this case it is Python). In
  MyRPC slang it is called generator. For available generators, see
  :ref:`features-target`.
* *CalculatorService* is the name of Python package where the
  generated files will go into. Actually, the interpretation of namespace
  is generator dependent, see :ref:`generators`.

Method
------

Our first method will calculate the sum of two integers::

  beginmethod sum
      in 0 required i32 a
      in 1 required i32 b
      out required i32
  endmethod

Explanation:

* *beginmethod* declares a method called *sum*.
* Methods can have zero or more input arguments, which are declared
  with *in* keyword. There are two input arguments: *a* and *b*. Both are
  *required*, meaning that they can't be null. If we allow null values,
  then *optional* keyword can be used instead. *i32* is the data type of
  arguments (32 bit signed integer). Integer numbers right after *in*
  are called field identifiers, or fids. During (de)serialization,
  MyRPC uses fids (*0* and *1*) instead of names (*a* and *b*) to identify input
  arguments. Fids must be unique and be between 0 ... 2\ :sup:`16` - 2.
* Return value is specified by *out*. In method declaration, exactly zero
  or one *out* keyword is allowed. If we don't have *out*,
  the method doesn't return value.

In place of *i32*, we can use any other primitive or user-defined type,
provided they are declared before. For more information on types, see
:ref:`typemapping`.

List
----

To allow variable number of input arguments, we can write generalized
version of the sum method by using list instead of separate *a* and *b*
arguments::

  list IntegerList i32

  beginmethod sum_list
      in 0 required IntegerList in_list
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

We can extend our IDL with a method, which classifies input argument::

  beginenum IntegerType
      entry IS_ZERO
      entry IS_NEGATIVE -1
      entry IS_POSITIVE 1
  endenum

  beginmethod classify
      in 0 required i32 a
      out required IntegerType
  endmethod

Explanation:

* Enumerations are started using *beginenum* declaration.
* One *entry* declaration is required per enumeration entry (or member).
* Enumeration entries can have an optional integer value (*-1* and *1*).
  If the value is not specified, then it will have the value of previous
  entry value + 1. The first entry of the enumeration has the default
  value of 0.

Structure
---------

The next one is a "batch" calculator example::

  beginenum OperationType
      entry ADD
      entry SUBSTRACT
      entry MULTIPLY
      entry DIVIDE
  endenum

  beginstruct Operation
      field 0 required OperationType op_type
      field 1 required float a
      field 2 required float b
  endstruct

  list OperationList Operation
  list ResultList float

  beginmethod batch_calculate
      in 0 required OperationList op_list
      out required ResultList
  endmethod

Explanation:

* *beginstruct* declares a structure called *Operation*.
* Field declarations inside structures are similar to argument
  declaration of methods, but instead of *in* and *out*, we have to use
  *field* keyword here.
* On instantiation, all fields will be set to null by default.

Exception
---------

Methods can throw exceptions. Exceptions typically represent some error
condition. Here is how you can declare them::

  beginexception DivideByZeroException
  endexception

  beginexception OtherException
      field 0 optional string message
  endexception

  beginmethod divide
      in 0 required float a
      in 1 required float b
      out required float
      throw DivideByZeroException
      throw OtherException
  endmethod

Explanation:

* *beginexception* declares exceptions called *DivideByZeroException* and
  *OtherException*.
* Exception declarations have the same syntax as structure declarations 
  (see above).
* Zero or more *throw* keywords inside *beginmethod*, each declaring
  what to throw.
* On instantiation, all fields will be set to null by default.

Comment
-------

The hash character (*#*) is used to start a comment in MyRPC IDL.

Invoke myrpcgen
---------------

Let's say, we have finished IDL and we would like to generate Python server
stub. To do it, execute:

.. code-block:: sh

   myrpcgen -g py -d gen-py -P calculator.idl

Explanation:

* *-g*: specify which generator to use. A *namespace* declaration is needed for
  each generator we would like to use, see :ref:`idlintro-namespace`.
* *-d*: output directory.
* *-P*: says that myrpcgen will generate server stub (aka processor). The opposite
  option would be *-C*, to generate client stub.
