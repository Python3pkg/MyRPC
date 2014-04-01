myrpc.util.ClientSubr = function(tr, codec)
{
    this._tr = tr;
    this._codec = codec;

    this._codec.set_transport(tr);
};

myrpc.util.ClientSubr.prototype.call = function(name, args_seri, result_seri, exc_handler, oncontinue, client)
{
    var oncontinue_func = function() {
	oncontinue(client);
    };

    this._exc = null;

    try {
	this._call(name, args_seri, result_seri, exc_handler, oncontinue_func);
    } catch (e) {
	if (e instanceof myrpc.common.MyRPCException) {
	    // Exceptions will be delayed until the call of call_continue. It provides
	    // simplified exception handling from the caller perspective.
	    //
	    // But beware: callers of this method should be prepared that the oncontinue
	    // callback can be executed immediately (and not only in the event loop).

	    this._exc = e;
	    oncontinue_func();
	} else {
	    throw e;
	}
    }
};

myrpc.util.ClientSubr.prototype.call_continue = function()
{
    var msg;
    var mtype;
    var exc_name;
    var err_msg = null;
    var exc = null;
    var r = null;

    // Re-throw delayed exceptions.

    if (this._exc)
	throw this._exc;

    // Process response.

    this._tr.set_state(myrpc.transport.TransportState.READ_BEGIN);

    msg = this._codec.read_message_begin();
    mtype = msg.get_mtype();

    switch (mtype) {
    case myrpc.codec.MessageType.CALL_RESPONSE:
	this._result_seri.myrpc_read(this._codec);
	break;

    case myrpc.codec.MessageType.CALL_EXCEPTION:
	exc_name = msg.get_name();
	exc = this._exc_handler(this._codec, exc_name);
	break;

    case myrpc.codec.MessageType.ERROR:
	err_msg = msg.get_err_msg();
	break;

    default:
	throw new myrpc.common.MessageHeaderException("Unexpected message type " + mtype);
    }

    this._codec.read_message_end();

    this._tr.set_state(myrpc.transport.TransportState.READ_END);

    // Check for ERROR message.

    if (err_msg != null)
	throw new myrpc.common.ServerErrorException(err_msg);

    // Throw exception or return normally.

    if (exc)
	throw exc;

    if ("get_result" in this._result_seri)
	r = this._result_seri.get_result();

    return r;
};

myrpc.util.ClientSubr.prototype._call = function(name, args_seri, result_seri, exc_handler, oncontinue)
{
    var msg;

    this._result_seri = result_seri;
    this._exc_handler = exc_handler;

    this._tr.set_oncontinue(oncontinue);

    // Serialize method call.

    this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);

    msg = new myrpc.codec.CallRequestMessage(name);
    this._codec.write_message_begin(msg);

    args_seri.myrpc_write(this._codec);

    this._codec.write_message_end();

    this._tr.set_state(myrpc.transport.TransportState.WRITE_END);
};
