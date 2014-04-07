myrpc.util.BufferIO = function(buf)
{
    // This class implements a memory-based buffer which has
    // file-like interface (e.g. read, write). Uint8Array is used
    // to provide binary buffer type.
    //
    // Buffering works as follows:
    //
    // |----------------|~~~~~~~~~~~~~|
    //    ^             ^             ^
    //    |             |             |
    //    +- this._pos  +- this._len  +- this._buf.length
    //       (r/w pos)     (data len)    (allocated buffer len)

    this.set_buffer(buf);
};

// Buffer write chunksize (must be power of 2).
myrpc.util.BufferIO._CHUNKSIZE = 1024;

myrpc.util.BufferIO.prototype.get_buffer = function()
{
    var buf = this._buf.subarray(0, this._len);

    return buf;
};

myrpc.util.BufferIO.prototype.set_buffer = function(buf)
{
    var bufcopy = buf ? new Uint8Array(buf) : new Uint8Array(0);

    this._buf = bufcopy;
    this._pos = 0;
    this._len = bufcopy.length;
};

myrpc.util.BufferIO.prototype.read = function(count)
{
    var pos = this._pos + count;
    var buf;

    // If the updated pos points behind data len, then
    // clamp pos to data len.

    if (pos > this._len)
	pos = this._len;

    buf = this._buf.subarray(this._pos, pos);
    this._pos = pos;

    return buf;
};

myrpc.util.BufferIO.prototype.write = function(buf)
{
    var pos = this._pos + buf.length;
    var newbuf;

    // If the updated pos points behind data len, then
    // increase data len to pos.

    if (pos > this._len)
	this._len = pos;

    // Resize buffer if pos points behind the allocated size of
    // buffer.

    if (pos > this._buf.length) {
	newbuf = new Uint8Array(this._align(pos));
	newbuf.set(this._buf);
	this._buf = newbuf;
    }

    this._buf.set(buf, this._pos);
    this._pos = pos;
};

myrpc.util.BufferIO.prototype._align = function(size)
{
    var mask = myrpc.util.BufferIO._CHUNKSIZE - 1;
    var asize = (size + mask) & ~mask;

    return asize;
};
