import struct

from myrpc.Common import MyRPCInternalException, MessageHeaderException, MessageDecodeException
from myrpc.codec.CodecBase import FID_STOP, MessageType, DataType, CallRequestMessage, CallResponseMessage, CallExceptionMessage, ErrorMessage, CodecBase

_SIGNATURE = 0x5341
_VERSION = 0x0001
_ENCODING = "utf-8"
_FORMAT = {"B": 1,
           "H": 2,
           "I": 4,
           "Q": 8,
           "b": 1,
           "h": 2,
           "i": 4,
           "q": 8,
           "f": 4,
           "d": 8}

class BinaryCodec(CodecBase):
    """Provide binary-based codec."""

    def __init__(self):
        super().__init__()

    def read_message_begin(self):
        signature = self.read_ui16()
        if signature != _SIGNATURE:
            raise MessageHeaderException("Invalid message signature")

        version = self.read_ui16()
        if version != _VERSION:
            raise MessageHeaderException("Unknown message version")

        mtype = self.read_ui8()
        if mtype == MessageType.CALL_REQUEST:
            name = self.read_string()
            msg = CallRequestMessage(name)
        elif mtype == MessageType.CALL_RESPONSE:
            msg = CallResponseMessage()
        elif mtype == MessageType.CALL_EXCEPTION:
            name = self.read_string()
            msg = CallExceptionMessage(name)
        elif mtype == MessageType.ERROR:
            err_msg = self.read_string()
            msg = ErrorMessage(err_msg)
        else:
            raise MessageHeaderException("Unknown message type {}".format(mtype))

        return msg

    def write_message_begin(self, msg):
        mtype = msg.get_mtype()

        self.write_ui16(_SIGNATURE)
        self.write_ui16(_VERSION)
        self.write_ui8(mtype)

        if mtype == MessageType.CALL_REQUEST:
            name = msg.get_name()
            self.write_string(name)
        elif mtype == MessageType.CALL_RESPONSE:
            pass
        elif mtype == MessageType.CALL_EXCEPTION:
            name = msg.get_name()
            self.write_string(name)
        elif mtype == MessageType.ERROR:
            err_msg = msg.get_err_msg()
            self.write_string(err_msg)
        else:
            raise MyRPCInternalException("Unknown message type ".format(mtype))

    def read_message_end(self):
        pass

    def write_message_end(self):
        pass

    def read_list_begin(self):
        llen = self.read_ui32()
        dtype = self._read_dtype()

        return (llen, dtype)

    def write_list_begin(self, llen, dtype):
        self.write_ui32(llen)
        self._write_dtype(dtype)

    def read_list_end(self):
        pass

    def write_list_end(self):
        pass

    def read_struct_begin(self):
        pass

    def write_struct_begin(self):
        pass

    def read_struct_end(self):
        pass

    def write_struct_end(self):
        pass

    def read_field_begin(self):
        fid = self.read_ui16()

        dtype = None
        if fid != FID_STOP:
            dtype = self._read_dtype()

        return (fid, dtype)

    def write_field_begin(self, fid, dtype):
        self.write_ui16(fid)
        self._write_dtype(dtype)

    def read_field_end(self):
        pass

    def write_field_end(self):
        pass

    def write_field_stop(self):
        self.write_ui16(FID_STOP)

    def read_binary(self):
        buflen = self.read_ui32()
        buf = self._tr.read(buflen)

        return buf

    def write_binary(self, buf):
        buflen = len(buf)
        self.write_ui32(buflen)
        self._tr.write(buf)

    def read_string(self):
        buf = self.read_binary()
        try:
            s = buf.decode(_ENCODING)
        except UnicodeError:
            raise MessageDecodeException("Can't decode unicode string")

        return s

    def write_string(self, s):
        buf = s.encode(_ENCODING)
        self.write_binary(buf)

    def read_bool(self):
        b = self.read_ui8()

        return (b != 0)

    def write_bool(self, b):
        self.write_ui8(1 if b else 0)

    def read_ui8(self):
        i = self._read_num("B")

        return i

    def write_ui8(self, i):
        self._write_num("B", i)

    def read_ui16(self):
        i = self._read_num("H")

        return i

    def write_ui16(self, i):
        self._write_num("H", i)

    def read_ui32(self):
        i = self._read_num("I")

        return i

    def write_ui32(self, i):
        self._write_num("I", i)

    def read_ui64(self):
        i = self._read_num("Q")

        return i

    def write_ui64(self, i):
        self._write_num("Q", i)

    def read_i8(self):
        i = self._read_num("b")

        return i

    def write_i8(self, i):
        self._write_num("b", i)

    def read_i16(self):
        i = self._read_num("h")

        return i

    def write_i16(self, i):
        self._write_num("h", i)

    def read_i32(self):
        i = self._read_num("i")

        return i

    def write_i32(self, i):
        self._write_num("i", i)

    def read_i64(self):
        i = self._read_num("q")

        return i

    def write_i64(self, i):
        self._write_num("q", i)

    def read_float(self):
        f = self._read_num("f")

        return f

    def write_float(self, f):
        self._write_num("f", f)

    def read_double(self):
        f = self._read_num("d")

        return f

    def write_double(self, f):
        self._write_num("d", f)

    def _read_dtype(self):
        dtype = self.read_ui8()
        if dtype >= DataType._MAX:
            raise MessageDecodeException("Unknown data type {}".format(dtype))

        return dtype

    def _write_dtype(self, dtype):
        if dtype >= DataType._MAX:
            raise MyRPCInternalException("Unknown data type ".format(dtype))

        self.write_ui8(dtype)

    def _read_num(self, fmt):
        buflen = _FORMAT[fmt]
        buf = self._tr.read(buflen)
        (n,) = struct.unpack("!" + fmt, buf)

        return n

    def _write_num(self, fmt, n):
        buf = struct.pack("!" + fmt, n)
        self._tr.write(buf)
