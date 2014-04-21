from myrpc.Common import MessageHeaderException, ServerErrorException
from myrpc.transport.TransportBase import TransportState
from myrpc.codec.CodecBase import MessageType, CallRequestMessage

class ClientSubr:
    """Client class for client applications."""

    def __init__(self, tr, codec):
        self._tr = tr
        self._codec = codec

        self._codec.set_transport(tr)

    def call(self, name, args_seri, result_seri, exc_handler):
        # Serialize method call.

        self._tr.set_state(TransportState.WRITE_BEGIN)

        msg = CallRequestMessage(name)
        self._codec.write_message_begin(msg)

        args_seri.myrpc_write(self._codec)

        self._codec.write_message_end()

        self._tr.set_state(TransportState.WRITE_END)

        # Process response.

        self._tr.set_state(TransportState.READ_BEGIN)

        err_msg = None
        exc = None
        r = None

        msg = self._codec.read_message_begin()
        mtype = msg.get_mtype()

        if mtype == MessageType.CALL_RESPONSE:
            result_seri.myrpc_read(self._codec)
        elif mtype == MessageType.CALL_EXCEPTION:
            exc_name = msg.get_name()
            exc = exc_handler(self._codec, exc_name)
        elif mtype == MessageType.ERROR:
            err_msg = msg.get_err_msg()
        else:
            raise MessageHeaderException("Unexpected message type {}".format(mtype))

        self._codec.read_message_end()

        self._tr.set_state(TransportState.READ_END)

        # Check for ERROR message.

        if err_msg != None:
            raise ServerErrorException(err_msg)

        # Throw exception or return normally.

        if exc:
            raise exc

        if hasattr(result_seri, "get_result"):
            r = result_seri.get_result()

        return r
