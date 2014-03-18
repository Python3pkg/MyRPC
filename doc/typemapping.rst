.. _typemapping:

Type mapping
============

The MyRPC IDL supports the following types, together with their language mappings:

+---------------------------------+-----------+--------------+---------------+
| Description                     | MyRPC     | Python       | JavaScript    |
+=================================+===========+==============+===============+
| Null value                      |           | None         | null          |
+---------------------------------+-----------+--------------+---------------+
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

.. [#py] See :ref:`generators-py` for more details.
.. [#js] See :ref:`generators-js` for more details.

Binary buffer, string, boolean, integer and floating point types are primitive
types. The remaining ones are user-defined types (except the null value).
