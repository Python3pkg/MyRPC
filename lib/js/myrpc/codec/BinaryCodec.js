myrpc.codec.BinaryCodec = function()
{
    myrpc.codec.CodecBase.call(this);
};

myrpc.codec.BinaryCodec.prototype = Object.create(myrpc.codec.CodecBase.prototype);
myrpc.codec.BinaryCodec.prototype.constructor = myrpc.codec.BinaryCodec;

myrpc.codec.BinaryCodec._SIGNATURE = 0x19800411;
myrpc.codec.BinaryCodec._FORMAT = {"B": [1, "getUint8",   "setUint8"],
				   "H": [2, "getUint16",  "setUint16"],
				   "I": [4, "getUint32",  "setUint32"],
				   "Q": [8, "getUint64",  "setUint64"], // FIXME
				   "b": [1, "getInt8",    "setInt8"],
				   "h": [2, "getInt16",   "setInt16"],
				   "i": [4, "getInt32",   "setInt32"],
				   "q": [8, "getInt64",   "setInt64"], // FIXME
				   "f": [4, "getFloat32", "setFloat32"],
				   "d": [8, "getFloat64", "setFloat64"]};

myrpc.codec.BinaryCodec.prototype.read_message_begin = function()
{
    var signature;
    var mtype;
    var name;
    var msg;

    signature = this.read_ui32();
    if (signature != myrpc.codec.BinaryCodec._SIGNATURE)
	throw new myrpc.codec.CodecException("Invalid message header");

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

    default:
	throw new myrpc.codec.CodecException("Invalid message type " + mtype);
    }

    return msg;
};

myrpc.codec.BinaryCodec.prototype.write_message_begin = function(msg)
{
    var mtype = msg.get_mtype();
    var name;

    this.write_ui32(myrpc.codec.BinaryCodec._SIGNATURE);
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
	    throw new myrpc.codec.CodecException("Can't decode unicode string");
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
    var i = this._read_num("Q");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_ui64 = function(i)
{
    this._write_num("Q", i);
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
    var i = this._read_num("q");

    return i;
};

myrpc.codec.BinaryCodec.prototype.write_i64 = function(i)
{
    this._write_num("q", i);
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
	throw new myrpc.codec.CodecException("Invalid data type " + dtype);

    return dtype;
};

myrpc.codec.BinaryCodec.prototype._write_dtype = function(dtype)
{
    if (dtype >= myrpc.codec.DataType._MAX)
	throw new myrpc.common.MyRPCInternalException("Unknown data type " + dtype);

    this.write_ui8(dtype);
};

myrpc.codec.BinaryCodec.prototype._read_num = function(fmt)
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

    n = dbuf[funcname](0, false);

    return n;
};

myrpc.codec.BinaryCodec.prototype._write_num = function(fmt, n)
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
