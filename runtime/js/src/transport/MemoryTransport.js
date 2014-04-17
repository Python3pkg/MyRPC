// MODULE_DEP ../Common
// MODULE_DEP ./TransportBase
// MODULE_DEP ../util/BufferIO
// MODULE_EXPORT

// FIXME: set_oncontinue present in interface (not needed).

myrpc.transport.MemoryTransport = function(buf)
{
    myrpc.transport.TransportBase.call(this);

    this._rbio = new myrpc.util.BufferIO(buf);
    this._wbio = new myrpc.util.BufferIO();
};

myrpc.transport.MemoryTransport.prototype = Object.create(myrpc.transport.TransportBase.prototype);
myrpc.transport.MemoryTransport.prototype.constructor = myrpc.transport.MemoryTransport;

myrpc.transport.MemoryTransport.prototype.set_state = function(state)
{
    switch (state) {
    case myrpc.transport.TransportState.READ_END:
	this._rbio.set_buffer();
	break;

    case myrpc.transport.TransportState.WRITE_BEGIN:
	this._wbio.set_buffer();
	break;
    }
};

myrpc.transport.MemoryTransport.prototype.read = function(count)
{
    var buf = this._rbio.read(count);

    if (count > buf.length)
	throw new myrpc.common.MessageTruncatedException();

    return buf;
};

myrpc.transport.MemoryTransport.prototype.write = function(buf)
{
    this._wbio.write(buf);
};

myrpc.transport.MemoryTransport.prototype.get_value = function()
{
    var buf = this._wbio.get_buffer();

    return buf;
};
