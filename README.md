# MyRPC: RPC Framework for Distributed Computing

MyRPC is a remote procedure call framework designed to easily connect heterogeneous systems.

## Short summary of MyRPC features

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

## Info

* Feature introduction: http://myrpc.readthedocs.org/en/latest/features.html
* Installation: http://myrpc.readthedocs.org/en/latest/install.html
* Sample code: http://myrpc.readthedocs.org/en/latest/examples.html
* License: http://myrpc.readthedocs.org/en/latest/license.html
* Full doc: http://myrpc.readthedocs.org

(This framework heavily borrows ideas from Apache Thrift, however
it is redesigned & rewritten from scratch).
