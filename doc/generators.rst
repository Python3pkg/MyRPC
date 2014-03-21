.. FIXME: Add client/processor API description per generator.

.. _generators:

Generator specific information
==============================

.. _generators-py:

Python
------

Namespace
^^^^^^^^^

Python generator interprets **namespace** IDL declaration as a package
name. If we have the following in IDL::

  namespace py TopPackage.SubPackage

then the following files will be created in the directory specified
with the :option:`-d` :file:`{outdir}` option of myrpcgen:

+-----------------------------------------------------+----------------------------------------------------------+
| File                                                | Description                                              |
+=====================================================+==========================================================+
| :file:`{outdir}/TopPackage/__init__.py`             | Empty file.                                              |
+-----------------------------------------------------+----------------------------------------------------------+
| :file:`{outdir}/TopPackage/SubPackage/__init__.py`  | Empty file.                                              |
+-----------------------------------------------------+----------------------------------------------------------+
| :file:`{outdir}/TopPackage/SubPackage/Types.py`     | (De)serializers for: method arguments, return values and |
|                                                     | for user-defined types. All the user-defined types will  |
|                                                     | be in the *TopPackage.SubPackage.Types* module.          |
+-----------------------------------------------------+----------------------------------------------------------+
| :file:`{outdir}/TopPackage/SubPackage/Processor.py` | Processor stub implementation (*Processor* class) and    |
|                                                     | abstract interface (*Interface* class) in the            |
|                                                     | *TopPackage.SubPackage.Processor* module.                |
+-----------------------------------------------------+----------------------------------------------------------+

Enumeration
^^^^^^^^^^^

If we have the following in IDL::

  beginenum Status
      entry OK
      entry FIRST_ERROR
      entry SECOND_ERROR 42
  endenum

The generated code will look like (:file:`Types.py`):

.. code-block:: py

   class Status:
       OK = 0
       FIRST_ERROR = 1
       SECOND_ERROR = 42

Structures and exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^

MyRPC generated structure and exception classes behave exactly the
same, with one exception: exception classes have *Exception* as their
parent class, but structures don't have parent class.

If we have the following in IDL::

  beginstruct UserInfo
      field 0 required string username
      ...
  endstruct

  beginexception SizeTooLarge
      field 0 required ui16 maxsize
      ...
  endexception

*UserInfo* and *SizeTooLarge* can be instantiated as the following:

.. code-block:: py

   from TopPackage.SubPackage.Types import UserInfo, SizeTooLarge

   obj = UserInfo()
   exc = SizeTooLarge()

Depending on :option:`-f` option of myrpcgen, fields can be accessed as shown
here:

+--------------+-----------------------------+--------------------------+
| Option value | Getter invocation           | Setter invocation        |
+==============+=============================+==========================+
| direct       | value = obj.username,       | obj.username = value,    |
|              | value = exc.maxsize         | exc.maxsize = value      |
+--------------+-----------------------------+--------------------------+
| capital      | value = obj.getUsername(),  | obj.setUsername(value),  |
|              | value = exc.getMaxsize()    | exc.setMaxsize(value)    |
+--------------+-----------------------------+--------------------------+
| underscore   | value = obj.get_username(), | obj.set_username(value), |
|              | value = exc.get_maxsize()   | exc.set_maxsize(value)   |
+--------------+-----------------------------+--------------------------+

.. _generators-js:

JavaScript
----------

Namespace
^^^^^^^^^

If we have the following in IDL::

  namespace js TopNS.SubNS

then the following files will be created in the directory specified
with the :option:`-d` :file:`{outdir}` option of myrpcgen:

+----------------------------+-----------------------------------------------------------+
| File                       | Description                                               |
+============================+===========================================================+
| :file:`{outdir}/Types.js`  | (De)serializers for: method arguments, return values and  |
|                            | for user-defined types. All the user-defined types will   |
|                            | be in the *TopNS.SubNS.Types* namespace.                  |
+----------------------------+-----------------------------------------------------------+
| :file:`{outdir}/Client.js` | Client stub implementation in *TopNS.SubNS.Client* class. |
+----------------------------+-----------------------------------------------------------+

64 bit unsigned and signed integers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integers in JavaScript are limited to -2\ :sup:`53` ... 2\ :sup:`53`, however
MyRPC runtime doesn't check range limitation. For more information, see
http://ecma262-5.com/ELS5_HTML.htm#Section_8.5.

Enumeration
^^^^^^^^^^^

If we have the following in IDL::

  beginenum Status
      entry OK
      entry FIRST_ERROR
      entry SECOND_ERROR 42
  endenum

The generated code will look like (:file:`Types.js`):

.. code-block:: js

   TopNS.SubNS.Types.Status = {
       OK: 0,
       FIRST_ERROR: 1,
       SECOND_ERROR: 42
   };

Structures and exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^

MyRPC generated structure and exception objects behave exactly the
same.

If we have the following in IDL::

  beginstruct UserInfo
      field 0 required string username
      ...
  endstruct

  beginexception SizeTooLarge
      field 0 required ui16 maxsize
      ...
  endexception

*UserInfo* and *SizeTooLarge* can be instantiated as the following:

.. code-block:: js

   var obj = new TopNS.SubNS.Types.UserInfo();
   var exc = new TopNS.SubNS.Types.SizeTooLarge();

Depending on :option:`-f` option of myrpcgen, fields can be accessed as shown
here:

+--------------+-----------------------------+--------------------------+
| Option value | Getter invocation           | Setter invocation        |
+==============+=============================+==========================+
| direct       | value = obj.username,       | obj.username = value,    |
|              | value = exc.maxsize         | exc.maxsize = value      |
+--------------+-----------------------------+--------------------------+
| capital      | value = obj.getUsername(),  | obj.setUsername(value),  |
|              | value = exc.getMaxsize()    | exc.setMaxsize(value)    |
+--------------+-----------------------------+--------------------------+
| underscore   | value = obj.get_username(), | obj.set_username(value), |
|              | value = exc.get_maxsize()   | exc.set_maxsize(value)   |
+--------------+-----------------------------+--------------------------+
