from myrpc.Common import MyRPCInternalException, MessageDecodeException, MessageHeaderException
from myrpc.transport.TransportBase import TransportState
from myrpc.codec.CodecBase import MessageType, CallResponseMessage, CallExceptionMessage, ErrorMessage

class HandlerReturn:
    """Handler return value class."""

    def __init__(self):
        self._finished = True
        self._exc = None
        self._exc_name = None
        self._result = None

    def get_finished(self):
        return self._finished

    def get_exc(self):
        return (self._exc, self._exc_name)

    def get_result(self):
        return self._result

    def set_notfinished(self):
        self._finished = False

    def set_exc(self, exc, exc_name):
        self._exc = exc
        self._exc_name = exc_name

    def set_result(self, result):
        self._result = result

class ProcessorSubr:
    """Processor class for server applications."""

    def __init__(self, methodmap):
        self._messagemap = {MessageType.CALL_REQUEST: (self._read_CALL_REQUEST,
                                                       self._process_CALL_REQUEST)}

        self._methodmap = methodmap

        self._reset()

    def process_one(self, tr, codec):
        """Process one message.

        process_one can be called even when we are in middle of
        async method execution. In this case, the execution is aborted,
        and processing of the new message begins.
        """

        self._reset()

        self._tr = tr
        self._codec = codec

        self._codec.set_transport(tr)

        try:
            # Read one message.

            mtype = self._read()
        except MessageDecodeException as e:
            # Handle decoding errors.

            err_msg = e.get_msg()
            msg = ErrorMessage(err_msg)

            self._tr.set_state(TransportState.WRITE_BEGIN)
            self._codec.write_message_begin(msg)
            self._codec.write_message_end()
            self._tr.set_state(TransportState.WRITE_END)

            return True

        # Process message.

        finished = self._process(mtype)
        if not finished:
            # If a method requests async execution, then store mtype. The reason
            # of not storing it earlier is: we don't have to reset mtype if
            # an exception happens during _read or _process.

            self._mtype = mtype

        return finished

    def call_continue(self, func, user_data):
        """Continuation method for async method execution."""

        if self._mtype != MessageType.CALL_REQUEST:
            raise ValueError("Not in asynchronous method call") # FIXME: Is it the correct exception class?

        finished = self._continue_CALL_REQUEST(func, user_data)
        if finished:
            # If we are finished, then don't allow more repeated calls to call_continue.

            self._reset()

        return finished

    def _read(self):
        # Read one message.

        self._tr.set_state(TransportState.READ_BEGIN)

        msg = self._codec.read_message_begin()
        mtype = msg.get_mtype()

        try:
            readfunc = self._messagemap[mtype][0]
        except KeyError:
            raise MessageHeaderException("Unexpected message type {}".format(mtype))

        readfunc(msg)

        self._codec.read_message_end()

        self._tr.set_state(TransportState.READ_END)

        return mtype

    def _process(self, mtype):
        processfunc = self._messagemap[mtype][1]
        finished = processfunc()

        return finished

    def _read_CALL_REQUEST(self, msg):
        name = msg.get_name()

        try:
            (args_seri_class, handler) = self._methodmap[name]
        except KeyError:
            raise MessageHeaderException("Unknown method name {}".format(name))

        # Deserialize method arguments. The actual method call will be happen in
        # process callback.

        args_seri = args_seri_class()
        args_seri.myrpc_read(self._codec)

        self._args_seri = args_seri
        self._handler = handler

    def _process_CALL_REQUEST(self):
        # Be careful when calling handler: any exception raised (either directly
        # or indirectly) in handler has to propagate thru without catching it. This
        # ensures that the caller of process_one gets noticed about the exception
        # (which is an error condition).
        #
        # However:
        #  - Exceptions defined in IDL are catched in handler, this is the normal
        #    behaviour.
        #  - MessageDecodeException is caught in process_one, and it means that we
        #    can't decode the message. An ErrorMessage will be sent back to the client
        #    in this case.

        hr = self._handler(self._args_seri, None, None)
        finished = self._make_call_response(hr)

        return finished

    def _continue_CALL_REQUEST(self, func, user_data):
        # See notes on _process_CALL_REQUEST.

        hr = self._handler(None, func, user_data)
        finished = self._make_call_response(hr)

        return finished

    def _make_call_response(self, hr):
        # If the method is not finished yet, then don't send response.

        if not hr.get_finished():
            return False

        (exc, exc_name) = hr.get_exc()
        r = hr.get_result()

        # Write response.

        self._tr.set_state(TransportState.WRITE_BEGIN)

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

        self._tr.set_state(TransportState.WRITE_END)

        return True

    def _reset(self):
        self._mtype = None
        self._args_seri = None
        self._handler = None

class ProcessorNotFinishedClass:
    """Class of ProcessorNotFinished."""

    def __init__(self):
        pass

# Special return value for RPC method implementations to signal
# asynchronous execution.
ProcessorNotFinished = ProcessorNotFinishedClass();
