myrpc.util.HandlerReturn = function()
{
    this._exc = null;
    this._exc_name = null;
    this._result = null;
};

myrpc.util.HandlerReturn.prototype.get_exc = function()
{
    return [this._exc, this._exc_name];
};

myrpc.util.HandlerReturn.prototype.get_result = function()
{
    return this._result;
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
    this._methodmap = methodmap;
};

myrpc.util.ProcessorSubr.prototype.process_one = function(tr, codec)
{
    var err_msg;
    var msg;

    this._tr = tr;
    this._codec = codec;

    this._codec.set_transport(tr);

    this._reset();

    try {
        this._process_one();
    } catch (e) {
	if (e instanceof myrpc.common.MessageDecodeException) {
	    // Handle decoding errors.

            err_msg = e.get_msg();
            msg = new myrpc.codec.ErrorMessage(err_msg);

            this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);
            this._codec.write_message_begin(msg);
            this._codec.write_message_end();
            this._tr.set_state(myrpc.transport.TransportState.WRITE_END);
	} else {
	    throw e;
	}
    }
};

myrpc.util.ProcessorSubr.prototype._process_one = function()
{
    var msg;
    var mtype;
    var cb;

    // Read one message.

    this._tr.set_state(myrpc.transport.TransportState.READ_BEGIN);

    msg = this._codec.read_message_begin();
    mtype = msg.get_mtype();

    switch (mtype) {
    case myrpc.codec.MessageType.CALL_REQUEST:
        this._process_CALL_REQUEST_read(msg);
	break;

    default:
        throw new myrpc.common.MessageHeaderException("Unexpected message type " + mtype);
    }

    this._codec.read_message_end();

    this._tr.set_state(myrpc.transport.TransportState.READ_END);

    // Write response.

    this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);

    cb = this._get_process_cb();
    cb();

    this._tr.set_state(myrpc.transport.TransportState.WRITE_END);
};

myrpc.util.ProcessorSubr.prototype._process_CALL_REQUEST_read = function(msg)
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

    // Deserialize method arguments. The actual method call will be happen in
    // _process_CALL_REQUEST_write.

    args_seri = new args_seri_class();
    args_seri.myrpc_read(this._codec);

    this._args_seri = args_seri;
    this._handler = handler;

    this._set_process_cb(myrpc.common.proxy(this._process_CALL_REQUEST_write, this));
};

myrpc.util.ProcessorSubr.prototype._process_CALL_REQUEST_write = function()
{
    // Be careful when calling handler: any exception raised (either directly
    // or indirectly) in handler has to propagate thru without catching it. This
    // ensures that the caller of ProcessorSubr.process_one gets noticed about the
    // exception (which is an error condition).
    //
    // However:
    //  - Exceptions defined in IDL are catched in handler, this is the normal
    //    behaviour.
    //  - MessageDecodeException is catched in ProcessorSubr.process_one, and it
    //    means that we can't decode the message. An ErrorMessage will be sent
    //    back to the client in this case.

    var hr;
    var excinfo;
    var exc;
    var exc_name;
    var r;
    var msg;

    hr = this._handler(this._args_seri);

    excinfo = hr.get_exc();
    exc = excinfo[0];
    exc_name = excinfo[1];

    r = hr.get_result();

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
};

myrpc.util.ProcessorSubr.prototype._reset = function()
{
    this._set_process_cb(null);
    this._args_seri = null;
    this._handler = null;
};

myrpc.util.ProcessorSubr.prototype._get_process_cb = function()
{
    return this._process_cb;
};

myrpc.util.ProcessorSubr.prototype._set_process_cb = function(cb)
{
    this._process_cb = cb;
};
