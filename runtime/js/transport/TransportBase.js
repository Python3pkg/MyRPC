// In transport implementation classes Uint8Array is used to provide
// binary data type.

myrpc.transport.TransportState = {
    READ_BEGIN  : 0,
    READ_END    : 1,
    WRITE_BEGIN : 2,
    WRITE_END   : 3
};

myrpc.transport.TransportBase = function()
{
    myrpc.common.abstract_class(this, myrpc.transport.TransportBase);
};

myrpc.transport.TransportBase.prototype.set_state = function(state)
{
};

myrpc.transport.TransportBase.prototype.read = function(count)
{
};

myrpc.transport.TransportBase.prototype.write = function(buf)
{
};

// JavaScript specific API method to set continue callback.
myrpc.transport.TransportBase.prototype.set_oncontinue = function(oncontinue)
{
};

myrpc.transport.TransportException = function(msg)
{
    myrpc.common.MyRPCException.call(this, msg);
};

myrpc.transport.TransportException.prototype = Object.create(myrpc.common.MyRPCException.prototype);
myrpc.transport.TransportException.prototype.constructor = myrpc.transport.TransportException;
