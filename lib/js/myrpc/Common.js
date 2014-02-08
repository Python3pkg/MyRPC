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

myrpc.common.SerializeException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.SerializeException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.SerializeException.prototype.constructor = myrpc.common.SerializeException;

myrpc.common.DeserializeException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.DeserializeException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.DeserializeException.prototype.constructor = myrpc.common.DeserializeException;

myrpc.common.MessageTruncatedException = function()
{
    myrpc.common.DeserializeException.call(this, "Message is truncated");
};

myrpc.common.MessageTruncatedException.prototype = Object.create(myrpc.common.DeserializeException.prototype);
myrpc.common.MessageTruncatedException.prototype.constructor = myrpc.common.MessageTruncatedException;

myrpc.common.MessageHeaderException = function(msg)
{
    myrpc.common.DeserializeException.call(this, msg);
};

myrpc.common.MessageHeaderException.prototype = Object.create(myrpc.common.DeserializeException.prototype);
myrpc.common.MessageHeaderException.prototype.constructor = myrpc.common.MessageHeaderException;

myrpc.common.MessageDecodeException = function(msg)
{
    myrpc.common.DeserializeException.call(this, msg);
};

myrpc.common.MessageDecodeException.prototype = Object.create(myrpc.common.DeserializeException.prototype);
myrpc.common.MessageDecodeException.prototype.constructor = myrpc.common.MessageDecodeException;

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
