myrpc.util.ClientSubr = function(tr, codec)
{
    this._tr = tr;
    this._codec = codec;

    this._codec.set_transport(tr);
};

myrpc.util.ClientSubr.prototype.call = function(name, args_seri, result_seri, exc_handler, oncontinue, client)
{
    var msg = new myrpc.codec.CallRequestMessage(name);

    this._result_seri = result_seri;
    this._exc_handler = exc_handler;

    this._tr.set_oncontinue(function() {
	oncontinue(client);
    });

    // Serialize method call.

    this._tr.set_state(myrpc.transport.TransportState.WRITE_BEGIN);

    this._codec.write_message_begin(msg);
    args_seri.write(this._codec);
    this._codec.write_message_end();

    this._tr.set_state(myrpc.transport.TransportState.WRITE_END);
};

myrpc.util.ClientSubr.prototype.call_continue = function()
{
    var msg;
    var mtype;
    var name;
    var has_exc = false;
    var r;

    // Process response.

    this._tr.set_state(myrpc.transport.TransportState.READ_BEGIN);

    msg = this._codec.read_message_begin();
    mtype = msg.get_mtype();

    switch (mtype) {
    case myrpc.codec.MessageType.CALL_RESPONSE:
	this._result_seri.read(this._codec);
	break;

    case myrpc.codec.MessageType.CALL_EXCEPTION:
	name = msg.get_name();
	this._exc_handler.read(this._codec, name);
	has_exc = true;
	break;

    default:
	throw new myrpc.common.MessageTypeException("Unexpected message type received " + mtype);
    }

    this._codec.read_message_end();

    this._tr.set_state(myrpc.transport.TransportState.READ_END);

    // Throw exception or return normally.

    if (has_exc)
	this._exc_handler.throw();

    // FIXME: hmmm
    if ("get_result" in this._result_seri) {
	r = this._result_seri.get_result();

	return r;
    }
};
