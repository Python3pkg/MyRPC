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

myrpc.common.MessageTypeException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.MessageTypeException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.MessageTypeException.prototype.constructor = myrpc.common.MessageTypeException;

myrpc.common.SerializerException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.SerializerException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.SerializerException.prototype.constructor = myrpc.common.SerializerException;

myrpc.common.DeserializerException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.common.DeserializerException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.common.DeserializerException.prototype.constructor = myrpc.common.DeserializerException;

myrpc.common.abstract_class = function(obj, constructor)
{
    if (obj.constructor == constructor)
	throw new myrpc.common.MyRPCInternalException("Can't instantiate abstract class"); // FIXME: firefox
};
