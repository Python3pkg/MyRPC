Features
========

Short summary of MyRPC features:

* No external dependencies.
* Multi-platform capability.
* IDL-based client/server stub generation.
* Binary capable (no need for escaping of binary data).
* Single roundtrip protocol, ideal for HTTP (but no limited to).
* Support various data types: string, binary, signed and unsigned
  integers, float, list, struct and enum.
* All data types are supported on all platforms.
* Support exceptions.
* Correct input validation of the received messages.
* Legacy free code (since we are new :).

Target languages
----------------

MyRPC supports the following target languages:

+-------------+------------------------+------------------------+
| Language    | Client stub generation | Server stub generation |
+=============+========================+========================+
| Python >= 3 | No                     | Yes                    |
+-------------+------------------------+------------------------+
| JavaScript  | Yes                    | No                     |
+-------------+------------------------+------------------------+
