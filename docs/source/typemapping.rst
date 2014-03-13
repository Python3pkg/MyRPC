Type mapping
============

The MyRPC IDL supports the following types, together with their language mappings:

+---------------------------------+-----------+--------------+---------------+
| Description                     | MyRPC     | Python       | JavaScript    |
+=================================+===========+==============+===============+
| Binary buffer                   | binary    | bytes        | Uint8Array    |
+---------------------------------+-----------+--------------+---------------+
| String                          | string    | str          | String        |
+---------------------------------+-----------+--------------+---------------+
| Boolean                         | bool      | True, False  | true, false   |
+---------------------------------+-----------+--------------+---------------+
| Unsigned integer, 8 bit         | ui8       | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Unsigned integer, 16 bit        | ui16      | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Unsigned integer, 32 bit        | ui32      | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Unsigned integer, 64 bit        | ui64      | int          | Number [#js]_ |
+---------------------------------+-----------+--------------+---------------+
| Signed integer, 8 bit           | i8        | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Signed integer, 16 bit          | i16       | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Signed integer, 32 bit          | i32       | int          | Number        |
+---------------------------------+-----------+--------------+---------------+
| Signed integer, 64 bit          | i64       | int          | Number [#js]_ |
+---------------------------------+-----------+--------------+---------------+
| Single precision floating point | float     | float        | Number        |
+---------------------------------+-----------+--------------+---------------+
| Double precision floating point | double    | float        | Number        |
+---------------------------------+-----------+--------------+---------------+
| Enumeration                     | enum      | class [#py]_ | Object [#js]_ |
+---------------------------------+-----------+--------------+---------------+
| List                            | list      | list         | Array         |
+---------------------------------+-----------+--------------+---------------+
| Structure                       | struct    | class [#py]_ | Object [#js]_ |
+---------------------------------+-----------+--------------+---------------+
| Exception                       | exception | class [#py]_ | Object [#js]_ |
+---------------------------------+-----------+--------------+---------------+

.. [#py] See :ref:`typemapping-py` for more details.
.. [#js] See :ref:`typemapping-js` for more details.

.. _typemapping-py:

Python
------

Enumeration
^^^^^^^^^^^

If we have the following in IDL::

  beginenum Status
      entry OK
      entry FIRST_ERROR
      entry SECOND_ERROR 42
  endenum

The generated code will look like:

.. code-block:: py

   class Status:
       OK = 0
       FIRST_ERROR = 1
       SECOND_ERROR = 42

Structure and exception
^^^^^^^^^^^^^^^^^^^^^^^

FIXME

.. _typemapping-js:

JavaScript
----------

64 bit unsigned and signed integers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integers in JavaScript are limited to -2\ :sup:`53` ... 2\ :sup:`53`, however
MyRPC runtime doesn't check range limitation. For more information, see
http://ecma262-5.com/ELS5_HTML.htm#Section_8.5.

Enumeration
^^^^^^^^^^^

If we have the following in IDL::

  namespace js MyService

  beginenum Status
      entry OK
      entry FIRST_ERROR
      entry SECOND_ERROR 42
  endenum

The generated code will look like:

.. code-block:: js

   MyService.Types.Status = {
       OK: 0,
       FIRST_ERROR: 1,
       SECOND_ERROR: 42
   };

Structure and exception
^^^^^^^^^^^^^^^^^^^^^^^

FIXME
