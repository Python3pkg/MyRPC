// FIXME: HTTPClientTransport is not yet supported under Node.js.

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
    var buf = this._rbio.read(count);

    if (count > buf.length)
	throw new myrpc.common.MessageTruncatedException();

    return buf;
};

myrpc.transport.HTTPClientTransport.prototype.write = function(buf)
{
    this._wbio.write(buf);
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

    this._rbio = null;
    this._wbio = new myrpc.util.BufferIO();
};

myrpc.transport.HTTPClientTransport.prototype._flush = function()
{
    var wbuf = this._wbio.get_buffer();
    var that = this;

    if (!this._oncontinue)
	throw new myrpc.common.MyRPCInternalException("oncontinue callback is null");

    this._xhr = new XMLHttpRequest();
    this._xhr.open("POST", this._url, true);
    this._xhr.setRequestHeader("Content-Type", "application/octet-stream");
    this._xhr.responseType = "arraybuffer";
    this._xhr.onreadystatechange = function() {
	var rbuf;

	if (that._xhr.readyState == 4) {
	    that._status = that._xhr.status;
	    if (that._is_status_ok()) {
		rbuf = new Uint8Array(that._xhr.response);
		that._rbio = new myrpc.util.BufferIO(rbuf);
	    }

	    // Do not abort already completed request (see _reset).
	    that._xhr = null;

	    that._oncontinue();
	}
    };
    if (this._timeout != null)
	this._xhr.timeout = this._timeout;
    this._xhr.send(wbuf);
};

myrpc.transport.HTTPClientTransport.prototype._check_status = function()
{
    if (!this._is_status_ok())
	throw new myrpc.transport.TransportException("HTTP request failed with status code " + this._status);
};

myrpc.transport.HTTPClientTransport.prototype._is_status_ok = function()
{
    var r = (this._status >= 200 && this._status < 300);

    return r;
};
