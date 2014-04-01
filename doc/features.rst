.. TODO: Keep feature list in-sync with setup.py.

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

+---------------+----------------+------------------------+------------------+------------------------------------+---------------------+
| Language      | Generator name | Client stub generation | Client stub mode | Processor stub generation [#proc]_ | Processor stub mode |
+===============+================+========================+==================+====================================+---------------------+
| Python >= 3.3 | py             | Yes                    | Sync             | Yes                                | Sync                |
+---------------+----------------+------------------------+------------------+------------------------------------+---------------------+
| JavaScript    | js             | Yes                    | Async            | No                                 |                     |
+---------------+----------------+------------------------+------------------+------------------------------------+---------------------+

.. [#proc] Also known as server stub. In MyRPC terminology it is called processor stub.
