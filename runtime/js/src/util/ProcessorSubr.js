// MODULE_DEP ../Common
// MODULE_DEP ../transport/TransportBase
// MODULE_DEP ../codec/CodecBase
// MODULE_EXPORT

myrpc.util.HandlerReturn = function()
{
    this._finished = true;
    this._exc = null;
    this._exc_name = null;
    this._result = null;
};

myrpc.util.HandlerReturn.prototype.get_finished = function()
{
    return this._finished;
};

myrpc.util.HandlerReturn.prototype.get_exc = function()
{
    return [this._exc, this._exc_name];
};

myrpc.util.HandlerReturn.prototype.get_result = function()
{
    return this._result;
};

myrpc.util.HandlerReturn.prototype.set_notfinished = function()
{
    this._finished = false;
};

myrpc.util.HandlerReturn.prototype.set_exc = function(exc, exc_name)
{
    this._exc = exc;
    this._exc_name = exc_name;
};

myrpc.util.HandlerReturn.prototype.set_result = function(result)
{
    this._result = result;
};

myrpc.util.ProcessorSubr = function(methodmap)
{
    // We store numeric keys in this._messagemap, and fortunately
    // they don't conflict with JavaScript built-in object members.

    this._messagemap = {};
    this._messagemap[myrpc.codec.MessageType.CALL_REQUEST] = [myrpc.common.proxy(this._read_CALL_REQUEST, this),
							      myrpc.common.proxy(this._process_CALL_REQUEST, this)];

    this._methodmap = methodmap;
};

myrpc.util.ProcessorSubr.prototype.process_one = function(tr, codec)
{
    // process_one can be called even when we are in middle of
    // async method execution. In this case, the execution is aborted,
    // and processing of the new message begins.

    var mtype;
    var err_msg;
    var msg;
    var finished;

    this._reset();

    this._tr = tr;
    this._codec = codec;

    this._codec.set_transport(tr);

    try {
	// Read one message.

        mtype = this._read();
    } catch (e) {
	if (e instanceof myrpc.common.MessageDecodeException) {
	    // Handle decoding errors.

            err_msg = e.get_msg();
            msg = new myrpc.codec.ErrorMessage(err_msg);

            this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);
            this._codec.write_message_begin(msg);
            this._codec.write_message_end();
            this._tr.set_state(myrpc.transport.TransportState.WRITE_END);

	    return true;
	} else {
	    throw e;
	}
    }

    // Process message.

    finished = this._process(mtype);
    if (!finished) {
	// If a method requests async execution, then store mtype. The reason
	// of not storing it earlier is: we don't have to reset mtype if
	// an exception happens during _read or _process.

	this._mtype = mtype;
    }

    return finished;
};

myrpc.util.ProcessorSubr.prototype.call_continue = function(func, user_data)
{
    // Continuation method for async method execution.

    var finished;

    if (this._mtype != myrpc.codec.MessageType.CALL_REQUEST)
	throw new myrpc.common.IllegalArgumentException("Not in asynchronous method call");

    finished = this._continue_CALL_REQUEST(func, user_data);
    if (finished) {
	// If we are finished, then don't allow more repeated calls to call_continue.

	this._reset();
    }

    return finished;
};

myrpc.util.ProcessorSubr.prototype._read = function()
{
    var msg;
    var mtype;
    var messageinfo;
    var readfunc;

    // Read one message.

    this._tr.set_state(myrpc.transport.TransportState.READ_BEGIN);

    msg = this._codec.read_message_begin();
    mtype = msg.get_mtype();

    if (!(mtype in this._messagemap))
        throw new myrpc.common.MessageHeaderException("Unexpected message type " + mtype);

    messageinfo = this._messagemap[mtype];
    readfunc = messageinfo[0];

    readfunc(msg);

    this._codec.read_message_end();

    this._tr.set_state(myrpc.transport.TransportState.READ_END);

    return mtype;
};

myrpc.util.ProcessorSubr.prototype._process = function(mtype)
{
    var messageinfo = this._messagemap[mtype];
    var processfunc = messageinfo[1];
    var finished = processfunc();

    return finished;
};

myrpc.util.ProcessorSubr.prototype._read_CALL_REQUEST = function(msg)
{
    var name = msg.get_name();
    var method_name = "myrpc_" + name;
    var methodinfo;
    var args_seri_class;
    var handler;
    var args_seri;

    if (!(method_name in this._methodmap))
	throw new myrpc.common.MessageHeaderException("Unknown method name " + name);

    methodinfo = this._methodmap[method_name];
    args_seri_class = methodinfo[0];
    handler = methodinfo[1];

    // Deserialize method arguments. The actual method call will happen in
    // process callback.

    args_seri = new args_seri_class();
    args_seri.myrpc_read(this._codec);

    this._args_seri = args_seri;
    this._handler = handler;
};

myrpc.util.ProcessorSubr.prototype._process_CALL_REQUEST = function()
{
    // Be careful when calling handler: any exception raised (either directly
    // or indirectly) in handler has to propagate thru without catching it. This
    // ensures that the caller of process_one gets noticed about the exception
    // (which is an error condition).
    //
    // However:
    //  - Exceptions defined in IDL are catched in handler, this is the normal
    //    behaviour.
    //  - MessageDecodeException is caught in process_one, and it means that we
    //    can't decode the message. An ErrorMessage will be sent back to the client
    //    in this case.

    var hr = this._handler(this._args_seri, null, null);
    var finished = this._make_call_response(hr);

    return finished;
};

myrpc.util.ProcessorSubr.prototype._continue_CALL_REQUEST = function(func, user_data)
{
    // See notes on _process_CALL_REQUEST.

    var hr = this._handler(null, func, user_data);
    var finished = this._make_call_response(hr);

    return finished;
};

myrpc.util.ProcessorSubr.prototype._make_call_response = function(hr)
{
    var excinfo;
    var exc;
    var exc_name;
    var r;
    var msg;

    // If the method is not finished yet, then don't send response.

    if (!hr.get_finished())
	return false;

    excinfo = hr.get_exc();
    exc = excinfo[0];
    exc_name = excinfo[1];

    r = hr.get_result();

    // Write response.

    this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);

    if (exc) {
        msg = new myrpc.codec.CallExceptionMessage(exc_name);
        this._codec.write_message_begin(msg);
        exc.myrpc_write(this._codec);
    } else if (r) {
        msg = new myrpc.codec.CallResponseMessage();
        this._codec.write_message_begin(msg);
        r.myrpc_write(this._codec);
    } else {
        throw new myrpc.common.MyRPCInternalException("Neither exc nor result is set");
    }

    this._codec.write_message_end();

    this._tr.set_state(myrpc.transport.TransportState.WRITE_END);

    return true;
};

myrpc.util.ProcessorSubr.prototype._reset = function()
{
    this._mtype = null;
    this._args_seri = null;
    this._handler = null;
};

myrpc.util.ProcessorNotFinishedClass = function()
{
};

// Special return value for RPC method implementations to signal
// asynchronous execution.
myrpc.util.ProcessorNotFinished = new myrpc.util.ProcessorNotFinishedClass();
