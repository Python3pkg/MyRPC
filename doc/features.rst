.. TODO: Keep feature list in-sync with README.md.

Features
========

Short summary of MyRPC features:

* No external dependencies.
* Cross-platform capability.
* IDL-based client and server stub generation.
* Binary capable (no need for escaping of binary data).
* Single roundtrip protocol, ideal for HTTP (but no limited to).
* Support various data types: string, binary, signed and unsigned
  integers, floating point, list, structure and enumeration.
* All data types are supported on all platforms.
* Support exceptions.
* Correct input validation of the received messages.
* Legacy free code (since we are new :).

.. _features-target:

Target languages
----------------

MyRPC supports the following target languages:

+-------------------+----------------+------------------------+------------+------------------------------------+----------------------+
| Language          | Generator name | Client stub generation | Client API | Processor stub generation [#proc]_ | Processor API [#lp]_ |
+===================+================+========================+============+====================================+======================+
| Python >= 3.3     | py             | Yes                    | Sync       | Yes                                | Sync                 |
+-------------------+----------------+------------------------+------------+------------------------------------+----------------------+
| JavaScript [#js]_ | js             | Yes                    | Async      | Yes                                | Sync and Async       |
+-------------------+----------------+------------------------+------------+------------------------------------+----------------------+

.. [#proc] Also known as server stub. In MyRPC terminology it is called processor stub.
.. [#lp] In case of HTTP, asynchronous processor API can be used to implement `long polling <http://en.wikipedia.org/wiki/Push_technology#Long_polling>`_.
.. [#js] Node.js and browsers are both supported.
