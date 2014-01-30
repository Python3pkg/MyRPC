// FIXME: Content-Length request/reply
// FIXME: xhr level 2 check
// FIXME: teszt 0 hosszusagu adatokra
// FIXME: XMLHttpRequest errorcallback test for != 200 http response (~ baj van vele sztem)

myrpc.transport.HTTPClientTransport = function(url)
{
    myrpc.transport.TransportBase.call(this);

    this._url = url;
    this._xhr = null;
    this._oncontinue = null;
    this._timeout = null;
};

myrpc.transport.HTTPClientTransport.prototype = Object.create(myrpc.transport.TransportBase.prototype);
myrpc.transport.HTTPClientTransport.prototype.constructor = myrpc.transport.HTTPClientTransport;

// HTTP write buffer size (must be power of 2).
myrpc.transport.HTTPClientTransport._CHUNKSIZE = 1024;

myrpc.transport.HTTPClientTransport.prototype.set_state = function(state)
{
    switch (state) {
    case myrpc.transport.TransportState.WRITE_BEGIN:
	this._reset();
	break;

    case myrpc.transport.TransportState.WRITE_END:
	this._flush();
	break;

    case myrpc.transport.TransportState.READ_BEGIN:
	this._check_status();
	break;
    }
};

myrpc.transport.HTTPClientTransport.prototype.read = function(count)
{
    var pos = this._rbufpos + count;
    var buf;

    if (pos > this._rbuf.length)
	throw new myrpc.transport.TransportException("EOF is reached");

    buf = this._rbuf.subarray(this._rbufpos, pos);
    this._rbufpos = pos;

    return buf;
};

myrpc.transport.HTTPClientTransport.prototype.write = function(buf)
{
    var pos = this._wbufpos + buf.length;
    var wbuf;

    // Resize write buffer if neccessary.

    if (pos > this._wbuf.length) {
	wbuf = new Uint8Array(this._align(pos));
	wbuf.set(this._wbuf);
	this._wbuf = wbuf;
    }

    this._wbuf.set(buf, this._wbufpos);
    this._wbufpos = pos;
};

myrpc.transport.HTTPClientTransport.prototype.set_oncontinue = function(oncontinue)
{
    this._oncontinue = oncontinue;
};

myrpc.transport.HTTPClientTransport.prototype.set_timeout = function(timeout)
{
    this._timeout = timeout;
};

myrpc.transport.HTTPClientTransport.prototype._reset = function()
{
    // Abort running request and reset transport.

    if (this._xhr) {
	this._xhr.abort();
	this._xhr = null;
    }

    this._rbuf = null;
    this._rbufpos = 0;

    this._wbuf = new Uint8Array(0);
    this._wbufpos = 0;
};

myrpc.transport.HTTPClientTransport.prototype._flush = function()
{
    var buf = this._wbuf.subarray(0, this._wbufpos);
    var that = this;

    if (!this._oncontinue)
	throw new myrpc.transport.TransportException("oncontinue callback is null");

    this._xhr = new XMLHttpRequest();
    this._xhr.open("POST", this._url, true);
    this._xhr.setRequestHeader("Content-Type", "application/octet-stream");
    this._xhr.responseType = "arraybuffer";
    this._xhr.onreadystatechange = function() {
	if (that._xhr.readyState == 4) {
	    that._status = that._xhr.status;
	    if (that._is_status_ok())
		that._rbuf = new Uint8Array(that._xhr.response);

	    // Do not abort already completed request (see _reset).
	    that._xhr = null;

	    that._oncontinue();
	}
    };
    if (this._timeout != null)
	this._xhr.timeout = this._timeout;
    this._xhr.send(buf);
};

myrpc.transport.HTTPClientTransport.prototype._check_status = function()
{
    if (!this._is_status_ok())
	throw new myrpc.transport.TransportException("HTTP request failed with status code " + this._status);
};

myrpc.transport.HTTPClientTransport.prototype._align = function(size)
{
    var mask = myrpc.transport.HTTPClientTransport._CHUNKSIZE - 1;
    var asize = (size + mask) & ~mask;

    return asize;
};

myrpc.transport.HTTPClientTransport.prototype._is_status_ok = function()
{
    var r = (this._status == 200);

    return r;
};
