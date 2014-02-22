myrpc.codec.BinaryCodec = function()
{
    myrpc.codec.CodecBase.call(this);
};

myrpc.codec.BinaryCodec.prototype = Object.create(myrpc.codec.CodecBase.prototype);
myrpc.codec.BinaryCodec.prototype.constructor = myrpc.codec.BinaryCodec;

myrpc.codec.BinaryCodec._SIGNATURE = 0x5341;
myrpc.codec.BinaryCodec._VERSION = 0x0001;

// DataView doesn't support 64 bit integers, therefore they have to be
// handled by custom methods.
myrpc.codec.BinaryCodec._FORMAT = {"B": [1, "getUint8",   "setUint8"],
				   "H": [2, "getUint16",  "setUint16"],
				   "I": [4, "getUint32",  "setUint32"],
				   "Q": [8, null,         null],
				   "b": [1, "getInt8",    "setInt8"],
				   "h": [2, "getInt16",   "setInt16"],
				   "i": [4, "getInt32",   "setInt32"],
				   "q": [8, null,         null],
				   "f": [4, "getFloat32", "setFloat32"],
				   "d": [8, "getFloat64", "setFloat64"]};
myrpc.codec.BinaryCodec._2_31 = Math.pow(2, 31);
myrpc.codec.BinaryCodec._2_32 = Math.pow(2, 32);

myrpc.codec.BinaryCodec.prototype.read_message_begin = function()
{
    var signature;
    var version;
    var mtype;
    var name;
    var err_msg;
    var msg;

    signature = this.read_ui16();
    if (signature != myrpc.codec.BinaryCodec._SIGNATURE)
	throw new myrpc.common.MessageHeaderException("Invalid message signature");

    version = this.read_ui16();
    if (version != myrpc.codec.BinaryCodec._VERSION)
	throw new myrpc.common.MessageHeaderException("Unknown message version");

    mtype = this.read_ui8();
    switch (mtype) {
    case myrpc.codec.MessageType.CALL_REQUEST:
	name = this.read_string();
	msg = new myrpc.codec.CallRequestMessage(name);
	break;

    case myrpc.codec.MessageType.CALL_RESPONSE:
	msg = new myrpc.codec.CallResponseMessage();
	break;

    case myrpc.codec.MessageType.CALL_EXCEPTION:
	name = this.read_string();
	msg = new myrpc.codec.CallExceptionMessage(name);
	break;

    case myrpc.codec.MessageType.ERROR:
	err_msg = this.read_string();
	msg = new myrpc.codec.ErrorMessage(err_msg);
	break;

    default:
	throw new myrpc.common.MessageHeaderException("Unknown message type " + mtype);
    }

    return msg;
};

myrpc.codec.BinaryCodec.prototype.write_message_begin = function(msg)
{
    var mtype = msg.get_mtype();
    var name;
    var err_msg;

    this.write_ui16(myrpc.codec.BinaryCodec._SIGNATURE);
    this.write_ui16(myrpc.codec.BinaryCodec._VERSION);
    this.write_ui8(mtype);

    switch (mtype) {
    case myrpc.codec.MessageType.CALL_REQUEST:
	name = msg.get_name();
	this.write_string(name);
	break;

    case myrpc.codec.MessageType.CALL_RESPONSE:
	break;

    case myrpc.codec.MessageType.CALL_EXCEPTION:
	name = msg.get_name();
	this.write_string(name);
	break;

    case myrpc.codec.MessageType.ERROR:
	err_msg = msg.get_err_msg();
	this.write_string(err_msg);
	break;

    default:
	throw new myrpc.common.MyRPCInternalException("Unknown message type " + mtype);
    }
};

myrpc.codec.BinaryCodec.prototype.read_message_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_message_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.read_list_begin = function()
{
    var llen = this.read_ui32();
    var dtype = this._read_dtype();

    return [llen, dtype];
};

myrpc.codec.BinaryCodec.prototype.write_list_begin = function(llen, dtype)
{
    this.write_ui32(llen);
    this._write_dtype(dtype);
};

myrpc.codec.BinaryCodec.prototype.read_list_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_list_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.read_struct_begin = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_struct_begin = function()
{
};

myrpc.codec.BinaryCodec.prototype.read_struct_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_struct_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.read_field_begin = function()
{
    var fid;
    var dtype = null;

    fid = this.read_ui16();
    if (fid != myrpc.codec.FID_STOP)
	dtype = this._read_dtype();

    return [fid, dtype];
};

myrpc.codec.BinaryCodec.prototype.write_field_begin = function(fid, dtype)
{
    this.write_ui16(fid);
    this._write_dtype(dtype);
};

myrpc.codec.BinaryCodec.prototype.read_field_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_field_end = function()
{
};

myrpc.codec.BinaryCodec.prototype.write_field_stop = function()
{
    this.write_ui16(myrpc.codec.FID_STOP);
};

myrpc.codec.BinaryCodec.prototype.read_binary = function()
{
    var buflen = this.read_ui32();
    var buf = this._tr.read(buflen);

    return buf;
};

myrpc.codec.BinaryCodec.prototype.write_binary = function(buf)
{
    var buflen = buf.length;
    this.write_ui32(buflen);
    this._tr.write(buf);
};

myrpc.codec.BinaryCodec.prototype.read_string = function()
{
    var buf = this.read_binary();
    var buflen = buf.length;
    var utf8 = "";
    var s;
    var i;

    for (i = 0; i < buflen; i++)
	utf8 += String.fromCharCode(buf[i]);

    try {
	s = decodeURIComponent(escape(utf8));
    } catch (e) {
	if (e instanceof URIError)
	    throw new myrpc.common.MessageBodyException("Can't decode unicode string");
	else
	    throw e;
    }

    return s;
};

myrpc.codec.BinaryCodec.prototype.write_string = function(s)
{
    var utf8 = unescape(encodeURIComponent(s));
    var buflen = utf8.length;
    var buf = new Uint8Array(buflen);
    var i;

    for (i = 0; i < buflen; i++)
	buf[i] = utf8.charCodeAt(i);

    this.write_binary(buf);
};

myrpc.codec.BinaryCodec.prototype.read_bool = function()
{
    var b = this.read_ui8();

    return (b != 0);
};

myrpc.codec.BinaryCodec.prototype.write_bool = function(b)
{
    this.write_ui8(b ? 1 : 0);
};

myrpc.codec.BinaryCodec.prototype.read_ui8 = function()
{
    var i = this._read_num("B");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_ui8 = function(i)
{
    this._write_num("B", i);
};

myrpc.codec.BinaryCodec.prototype.read_ui16 = function()
{
    var i = this._read_num("H");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_ui16 = function(i)
{
    this._write_num("H", i);
};

myrpc.codec.BinaryCodec.prototype.read_ui32 = function()
{
    var i = this._read_num("I");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_ui32 = function(i)
{
    this._write_num("I", i);
};

myrpc.codec.BinaryCodec.prototype.read_ui64 = function()
{
    var i = this._read_num("Q", this._read_ui64);

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_ui64 = function(i)
{
    this._write_num("Q", i, this._write_ui64);
};

myrpc.codec.BinaryCodec.prototype.read_i8 = function()
{
    var i = this._read_num("b");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_i8 = function(i)
{
    this._write_num("b", i);
};

myrpc.codec.BinaryCodec.prototype.read_i16 = function()
{
    var i = this._read_num("h");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_i16 = function(i)
{
    this._write_num("h", i);
};

myrpc.codec.BinaryCodec.prototype.read_i32 = function()
{
    var i = this._read_num("i");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_i32 = function(i)
{
    this._write_num("i", i);
};

myrpc.codec.BinaryCodec.prototype.read_i64 = function()
{
    var i = this._read_num("q", this._read_i64);

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_i64 = function(i)
{
    this._write_num("q", i, this._write_i64);
};

myrpc.codec.BinaryCodec.prototype.read_float = function()
{
    var f = this._read_num("f");

    return f;
};

myrpc.codec.BinaryCodec.prototype.write_float = function(f)
{
    this._write_num("f", f);
};

myrpc.codec.BinaryCodec.prototype.read_double = function()
{
    var f = this._read_num("d");

    return f;
};

myrpc.codec.BinaryCodec.prototype.write_double = function(f)
{
    this._write_num("d", f);
};

myrpc.codec.BinaryCodec.prototype._read_dtype = function()
{
    var dtype = this.read_ui8();
    if (dtype >= myrpc.codec.DataType._MAX)
	throw new myrpc.common.MessageBodyException("Unknown data type " + dtype);

    return dtype;
};

myrpc.codec.BinaryCodec.prototype._write_dtype = function(dtype)
{
    if (dtype >= myrpc.codec.DataType._MAX)
	throw new myrpc.common.MyRPCInternalException("Unknown data type " + dtype);

    this.write_ui8(dtype);
};

myrpc.codec.BinaryCodec.prototype._read_num = function(fmt, func)
{
    var fmtprop = this._lookup_format(fmt);
    var buflen;
    var funcname;
    var bbuf;
    var dbuf;
    var n;

    buflen = fmtprop[0];
    funcname = fmtprop[1];

    bbuf = this._tr.read(buflen);
    dbuf = new DataView(bbuf.buffer, bbuf.byteOffset, bbuf.length);

    n = func ? func.call(this, dbuf) : dbuf[funcname](0, false);

    return n;
};

myrpc.codec.BinaryCodec.prototype._write_num = function(fmt, n, func)
{
    var fmtprop = this._lookup_format(fmt);
    var buflen;
    var funcname;
    var abuf;
    var dbuf;
    var bbuf;

    buflen = fmtprop[0];
    funcname = fmtprop[2];

    abuf = new ArrayBuffer(buflen);
    dbuf = new DataView(abuf);
    bbuf = new Uint8Array(abuf);

    if (func)
	func.call(this, dbuf, n);
    else
	dbuf[funcname](0, n, false);

    this._tr.write(bbuf);
};

myrpc.codec.BinaryCodec.prototype._lookup_format = function(fmt)
{
    var fmtprop = myrpc.codec.BinaryCodec._FORMAT[fmt];
    if (!fmtprop)
	throw new myrpc.common.MyRPCInternalException("Unknown number format " + fmt);

    return fmtprop;
};

myrpc.codec.BinaryCodec.prototype._read_ui64 = function(dbuf)
{
    var i = this._read_64(dbuf, false);

    return i;
};

myrpc.codec.BinaryCodec.prototype._write_ui64 = function(dbuf, i)
{
    this._write_64(dbuf, false, i);
};

myrpc.codec.BinaryCodec.prototype._read_i64 = function(dbuf)
{
    var i = this._read_64(dbuf, true);

    return i;
};

myrpc.codec.BinaryCodec.prototype._write_i64 = function(dbuf, i)
{
    this._write_64(dbuf, true, i);
};

myrpc.codec.BinaryCodec.prototype._read_64 = function(dbuf, signed)
{
    var msb = dbuf.getUint32(0, false);
    var lsb = dbuf.getUint32(4, false);
    var neg = false;
    var i;

    if (signed && (msb & myrpc.codec.BinaryCodec._2_31)) {
	// MSB bit is 1, convert two's complement binary to JavaScript number.

	msb = this._negate_32(msb);
	lsb = this._negate_32(lsb);

	neg = true;
    }

    i = msb * myrpc.codec.BinaryCodec._2_32 + lsb;
    if (neg)
	i = -(i + 1);

    return i;
};

myrpc.codec.BinaryCodec.prototype._write_64 = function(dbuf, signed, i)
{
    var msb;
    var lsb;
    var neg = false;

    if (signed && (i < 0)) {
	// Negative number, convert to two's complement binary.

	i = -(i + 1);

	neg = true;
    }

    lsb = i % myrpc.codec.BinaryCodec._2_32;
    msb = (i - lsb) / myrpc.codec.BinaryCodec._2_32;

    if (neg) {
	msb = this._negate_32(msb);
	lsb = this._negate_32(lsb);
    }

    dbuf.setUint32(0, msb, false);
    dbuf.setUint32(4, lsb, false);
};

myrpc.codec.BinaryCodec.prototype._negate_32 = function(i)
{
    // Calculate one's complement. MSB bit hacking is neccessary because
    // JavaScript interprets bitwise negation result as signed.

    var ni = ~(i | myrpc.codec.BinaryCodec._2_31);

    if (!(i & myrpc.codec.BinaryCodec._2_31))
	ni += myrpc.codec.BinaryCodec._2_31;

    return ni;
};
