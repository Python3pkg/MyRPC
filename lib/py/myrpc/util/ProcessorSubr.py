# FIXME: error reporting: send packet back or throw exc? milyen exc-eket dobhat a process_one?
# FIXME: error handling: set transport state on error?
# FIXME: hibalehetoseg method_handlers exceptiont dob (pl. KeyError) akkor azt mi lehet hogy felreertelmezzuk...
# FIXME: importok atnezese...
# FIXME: ne kelljen mindig uj Processor obj ha a tr/codec valtozik
# FIXME: HandlerReturn state check

from myrpc.Common import MyRPCInternalException, MessageTypeException
from myrpc.transport.TransportBase import TransportState
from myrpc.codec.CodecBase import MessageType, CallResponseMessage, CallExceptionMessage

class HandlerReturn:
    """Handler return value class."""

    def __init__(self):
        self._exc = None
        self._exc_name = None
        self._result = None

    def get_exc(self):
        return (self._exc, self._exc_name)

    def get_result(self):
        return self._result

    def set_exc(self, exc, exc_name):
        self._exc = exc
        self._exc_name = exc_name

    def set_result(self, result):
        self._result = result

class ProcessorSubr:
    """Processor class for server applications."""

    def __init__(self, tr, codec, handlers):
        self._tr = tr
        self._codec = codec
        self._handlers = handlers

        self._codec.set_transport(tr)

    def process_one(self):
        # Read one packet.

        self._reset()

        self._tr.set_state(TransportState.READ_BEGIN)

        msg = self._codec.read_message_begin()
        mtype = msg.get_mtype()

        if mtype == MessageType.CALL_REQUEST:
            name = msg.get_name()
            self._process_CALL_REQUEST_read(name)
        else:
            raise MessageTypeException("Unexpected message type received {}".format(mtype))

        self._codec.read_message_end()

        self._tr.set_state(TransportState.READ_END)

        # Write response.

        self._tr.set_state(TransportState.WRITE_BEGIN)

        cb = self._get_process_cb()
        cb()

        self._tr.set_state(TransportState.WRITE_END)

    def _process_CALL_REQUEST_read(self, name):
        try:
            handler = self._handlers[name]
        except KeyError:
            raise MessageTypeException("Invalid method name received {}".format(name)) # FIXME: nem ideillo exctype

        self._curr_return = handler(self._codec)

        self._set_process_cb(self._process_CALL_REQUEST_write)

    def _process_CALL_REQUEST_write(self):
        (exc, exc_name) = self._curr_return.get_exc()
        r = self._curr_return.get_result()

        if exc:
            msg = CallExceptionMessage(exc_name)
            self._codec.write_message_begin(msg)
            exc.write(self._codec)
        elif r:
            msg = CallResponseMessage()
            self._codec.write_message_begin(msg)
            r.write(self._codec)
        else:
            raise MyRPCInternalException("Neither exc nor result is set")

        self._codec.write_message_end()

    def _reset(self):
        self._set_process_cb(None)
        self._curr_return = None

    def _get_process_cb(self):
        return self._process_cb

    def _set_process_cb(self, cb):
        self._process_cb = cb
