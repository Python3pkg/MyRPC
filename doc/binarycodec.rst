BinaryCodec implementation notes
================================

BinaryCodec has the following implementation details and limits:

* Message type is 8 bits.
* Field identifiers are 16 bits.
* Data type is 8 bits.
* Maximal size of binary and string (in encoded format) is 2\ :sup:`32` - 1 bytes.
* Maximal number of list elements is 2\ :sup:`32` - 1.
* Enums are 32 bit signed integers.
* Numbers are transmitted in network byte order.
