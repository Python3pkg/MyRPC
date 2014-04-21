from abc import ABCMeta, abstractmethod

FID_STOP = 0xffff

class MessageType:
    """Represent message type.

    Type can be:
     - CALL_REQUEST: call method request.
     - CALL_RESPONSE: reply to CALL_REQUEST, successful method call.
     - CALL_EXCEPTION: reply to CALL_REQUEST, exception thrown during execution.
     - ERROR: reply to all client messages, used for error reporting.
    """

    (CALL_REQUEST,
     CALL_RESPONSE,
     CALL_EXCEPTION,
     ERROR) = range(4)

class DataType:
    """Data type enum."""

    (BINARY,
     STRING,
     BOOL,
     UI8,
     UI16,
     UI32,
     UI64,
     I8,
     I16,
     I32,
     I64,
     FLOAT,
     DOUBLE,
     ENUM,
     LIST,
     STRUCT,
     _MAX) = range(17)

class MessageBase(metaclass = ABCMeta):
    """Base class for messages.

    Message classes represent only information, the actual
    (de)serialization is done in codec implementation classes.
    """

    @abstractmethod
    def __init__(self, mtype):
        self._mtype = mtype

    def get_mtype(self):
        return self._mtype

class CallRequestMessage(MessageBase):
    """CALL_REQUEST message (name: method to call)."""

    def __init__(self, name):
        super().__init__(MessageType.CALL_REQUEST)

        self._name = name

    def get_name(self):
        return self._name

class CallResponseMessage(MessageBase):
    """CALL_RESPONSE message."""

    def __init__(self):
        super().__init__(MessageType.CALL_RESPONSE)

class CallExceptionMessage(MessageBase):
    """CALL_EXCEPTION message (name: exception to throw)."""

    def __init__(self, name):
        super().__init__(MessageType.CALL_EXCEPTION)

        self._name = name

    def get_name(self):
        return self._name

class ErrorMessage(MessageBase):
    """ERROR message (err_msg: error message)."""

    def __init__(self, err_msg):
        super().__init__(MessageType.ERROR)

        self._err_msg = err_msg

    def get_err_msg(self):
        return self._err_msg

class CodecBase(metaclass = ABCMeta):
    """Base class for codec implementation classes.

    Design decisions:
     - This class abstracts high-level I/O (e.g. string).
     - Implementations inherit this class.
     - In case of error, implementations throw CodecException (or
       subclass).
    """

    def __init__(self):
        self._tr = None

    def set_transport(self, tr):
        self._tr = tr

    @abstractmethod
    def read_message_begin(self):
        pass

    @abstractmethod
    def write_message_begin(self, msg):
        pass

    @abstractmethod
    def read_message_end(self):
        pass

    @abstractmethod
    def write_message_end(self):
        pass

    @abstractmethod
    def read_list_begin(self):
        pass

    @abstractmethod
    def write_list_begin(self, llen, dtype):
        pass

    @abstractmethod
    def read_list_end(self):
        pass

    @abstractmethod
    def write_list_end(self):
        pass

    @abstractmethod
    def read_struct_begin(self):
        pass

    @abstractmethod
    def write_struct_begin(self):
        pass

    @abstractmethod
    def read_struct_end(self):
        pass

    @abstractmethod
    def write_struct_end(self):
        pass

    @abstractmethod
    def read_field_begin(self):
        pass

    @abstractmethod
    def write_field_begin(self, fid, dtype):
        pass

    @abstractmethod
    def read_field_end(self):
        pass

    @abstractmethod
    def write_field_end(self):
        pass

    @abstractmethod
    def write_field_stop(self):
        pass

    @abstractmethod
    def read_binary(self):
        pass

    @abstractmethod
    def write_binary(self, buf):
        pass

    @abstractmethod
    def read_string(self):
        pass

    @abstractmethod
    def write_string(self, s):
        pass

    @abstractmethod
    def read_bool(self):
        pass

    @abstractmethod
    def write_bool(self, b):
        pass

    @abstractmethod
    def read_ui8(self):
        pass

    @abstractmethod
    def write_ui8(self, i):
        pass

    @abstractmethod
    def read_ui16(self):
        pass

    @abstractmethod
    def write_ui16(self, i):
        pass

    @abstractmethod
    def read_ui32(self):
        pass

    @abstractmethod
    def write_ui32(self, i):
        pass

    @abstractmethod
    def read_ui64(self):
        pass

    @abstractmethod
    def write_ui64(self, i):
        pass

    @abstractmethod
    def read_i8(self):
        pass

    @abstractmethod
    def write_i8(self, i):
        pass

    @abstractmethod
    def read_i16(self):
        pass

    @abstractmethod
    def write_i16(self, i):
        pass

    @abstractmethod
    def read_i32(self):
        pass

    @abstractmethod
    def write_i32(self, i):
        pass

    @abstractmethod
    def read_i64(self):
        pass

    @abstractmethod
    def write_i64(self, i):
        pass

    @abstractmethod
    def read_float(self):
        pass

    @abstractmethod
    def write_float(self, f):
        pass

    @abstractmethod
    def read_double(self):
        pass

    @abstractmethod
    def write_double(self, f):
        pass
