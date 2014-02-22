# FIXME: ne kelljen mindig uj Processor obj ha a tr/codec valtozik
# FIXME: HandlerReturn state check

from myrpc.Common import MyRPCInternalException, MessageDecodeException, MessageHeaderException
from myrpc.transport.TransportBase import TransportState
from myrpc.codec.CodecBase import MessageType, CallResponseMessage, CallExceptionMessage, ErrorMessage

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

    def __init__(self, tr, codec, methodmap):
        self._tr = tr
        self._codec = codec
        self._methodmap = methodmap

        self._codec.set_transport(tr)

    def process_one(self):
        self._reset()

        try:
            self._process_one()
        except MessageDecodeException as e:
            # Handle decoding errors.

            err_msg = e.get_msg()
            msg = ErrorMessage(err_msg)

            self._tr.set_state(TransportState.WRITE_BEGIN)
            self._codec.write_message_begin(msg)
            self._codec.write_message_end()
            self._tr.set_state(TransportState.WRITE_END)

    def _process_one(self):
        # Read one message.

        self._tr.set_state(TransportState.READ_BEGIN)

        msg = self._codec.read_message_begin()
        mtype = msg.get_mtype()

        if mtype == MessageType.CALL_REQUEST:
            self._process_CALL_REQUEST_read(msg)
        else:
            raise MessageHeaderException("Unexpected message type {}".format(mtype))

        self._codec.read_message_end()

        self._tr.set_state(TransportState.READ_END)

        # Write response.

        self._tr.set_state(TransportState.WRITE_BEGIN)

        cb = self._get_process_cb()
        cb()

        self._tr.set_state(TransportState.WRITE_END)

    def _process_CALL_REQUEST_read(self, msg):
        name = msg.get_name()

        try:
            (args_seri_create, handler) = self._methodmap[name]
        except KeyError:
            raise MessageHeaderException("Unknown method name {}".format(name))

        # Deserialize method arguments. The actual method call will be happen in
        # _process_CALL_REQUEST_write.

        args_seri = args_seri_create()
        args_seri.myrpc_read(self._codec)

        self._args_seri = args_seri
        self._handler = handler

        self._set_process_cb(self._process_CALL_REQUEST_write)

    def _process_CALL_REQUEST_write(self):
        # Be careful when calling handler: any exception raised (either directly
        # or indirectly) in handler has to propagate thru without catching it. This
        # ensures that the caller of ProcessorSubr.process_one gets noticed about the
        # exception (which is an error condition).
        #
        # However:
        #  - Exceptions defined in IDL are catched in handler, this is the normal
        #    behaviour.
        #  - MessageDecodeException is catched in ProcessorSubr.process_one, and it
        #    means that we can't decode the message. An ErrorMessage will be sent
        #    back to the client in this case.

        hr = self._handler(self._args_seri)

        (exc, exc_name) = hr.get_exc()
        r = hr.get_result()

        if exc:
            msg = CallExceptionMessage(exc_name)
            self._codec.write_message_begin(msg)
            exc.myrpc_write(self._codec)
        elif r:
            msg = CallResponseMessage()
            self._codec.write_message_begin(msg)
            r.myrpc_write(self._codec)
        else:
            raise MyRPCInternalException("Neither exc nor result is set")

        self._codec.write_message_end()

    def _reset(self):
        self._set_process_cb(None)
        self._args_seri = None
        self._handler = None

    def _get_process_cb(self):
        return self._process_cb

    def _set_process_cb(self, cb):
        self._process_cb = cb
