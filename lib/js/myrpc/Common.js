myrpc.common.MyRPCException = function(msg)
{
    this._msg = msg;
};

myrpc.common.MyRPCException.prototype.get_msg = function()
{
    return this._msg;
};

myrpc.common.MyRPCInternalException = function(msg)
{
    this._msg = msg;
};

myrpc.common.MyRPCInternalException.prototype.get_msg = function()
{
    return this._msg;
};

myrpc.common.MessageEncodeException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.MessageEncodeException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.MessageEncodeException.prototype.constructor = myrpc.common.MessageEncodeException;

myrpc.common.MessageDecodeException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.MessageDecodeException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.MessageDecodeException.prototype.constructor = myrpc.common.MessageDecodeException;

myrpc.common.MessageTruncatedException = function()
{
    myrpc.common.MessageDecodeException.call(this, "Message is truncated");
};

myrpc.common.MessageTruncatedException.prototype = Object.create(myrpc.common.MessageDecodeException.prototype);
myrpc.common.MessageTruncatedException.prototype.constructor = myrpc.common.MessageTruncatedException;

myrpc.common.MessageHeaderException = function(msg)
{
    myrpc.common.MessageDecodeException.call(this, msg);
};

myrpc.common.MessageHeaderException.prototype = Object.create(myrpc.common.MessageDecodeException.prototype);
myrpc.common.MessageHeaderException.prototype.constructor = myrpc.common.MessageHeaderException;

myrpc.common.MessageBodyException = function(msg)
{
    myrpc.common.MessageDecodeException.call(this, msg);
};

myrpc.common.MessageBodyException.prototype = Object.create(myrpc.common.MessageDecodeException.prototype);
myrpc.common.MessageBodyException.prototype.constructor = myrpc.common.MessageBodyException;

myrpc.common.ServerErrorException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.ServerErrorException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.ServerErrorException.prototype.constructor = myrpc.common.ServerErrorException;

myrpc.common.abstract_class = function(obj, constructor)
{
    if (obj.constructor == constructor)
	throw new myrpc.common.MyRPCInternalException("Can't instantiate abstract class");
};
