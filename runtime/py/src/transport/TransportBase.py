from abc import ABCMeta, abstractmethod

from myrpc.Common import MyRPCException

class TransportState:
    """Represent the state of the transport.

    State is used for controlling transport I/O:
     - READ_BEGIN: receive a packet and store into read buffer.
     - READ_END: read ended, transport can drop its read buffer.
     - WRITE_BEGIN: empty send buffer, and begin buffering write data.
     - WRITE_END: writing completed, send packet.

    read() calls are allowed only between READ_BEGIN...READ_END, and
    write() calls are allowed only between WRITE_BEGIN...WRITE_END.

    Packetization (if needed) must be done at transport layer.
    """

    (READ_BEGIN,
     READ_END,
     WRITE_BEGIN,
     WRITE_END) = list(range(4))

class TransportBase(metaclass = ABCMeta):
    """Base class for transport implementation classes.

    Design decisions:
     - This class abstracts byte-level I/O.
     - Implementations inherit this class.
     - In case of I/O error, implementations throw TransportException (or
       subclass).
    """

    def __init__(self):
        pass

    @abstractmethod
    def set_state(self, state):
        pass

    @abstractmethod
    def read(self, count):
        """Read count bytes from transport.

        If less than count bytes is available (e.g. EOF, socket is closed), then
        implementations throw exception.
        """

        pass

    @abstractmethod
    def write(self, buf):
        pass

class TransportException(MyRPCException):
    """Base class for transport exception classes."""

    def __init__(self, msg):
        super().__init__(msg)
