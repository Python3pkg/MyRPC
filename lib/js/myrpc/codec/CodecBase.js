myrpc.codec.FID_STOP = 0xffff;

myrpc.codec.MessageType = {
    CALL_REQUEST   : 0,
    CALL_RESPONSE  : 1,
    CALL_EXCEPTION : 2,
    ERROR          : 3
};

myrpc.codec.DataType = {
    BINARY : 0,
    STRING : 1,
    BOOL   : 2,
    UI8    : 3,
    UI16   : 4,
    UI32   : 5,
    UI64   : 6,
    I8     : 7,
    I16    : 8,
    I32    : 9,
    I64    : 10,
    FLOAT  : 11,
    DOUBLE : 12,
    ENUM   : 13,
    LIST   : 14,
    STRUCT : 15,
    _MAX   : 16
};

myrpc.codec.MessageBase = function(mtype)
{
    myrpc.common.abstract_class(this, myrpc.codec.MessageBase);

    this._mtype = mtype;
};

myrpc.codec.MessageBase.prototype.get_mtype = function()
{
    return this._mtype;
};

myrpc.codec.CallRequestMessage = function(name)
{
    myrpc.codec.MessageBase.call(this, myrpc.codec.MessageType.CALL_REQUEST);

    this._name = name;
};

myrpc.codec.CallRequestMessage.prototype = Object.create(myrpc.codec.MessageBase.prototype);
myrpc.codec.CallRequestMessage.prototype.constructor = myrpc.codec.CallRequestMessage;

myrpc.codec.CallRequestMessage.prototype.get_name = function()
{
    return this._name;
};

myrpc.codec.CallResponseMessage = function()
{
    myrpc.codec.MessageBase.call(this, myrpc.codec.MessageType.CALL_RESPONSE);
};

myrpc.codec.CallResponseMessage.prototype = Object.create(myrpc.codec.MessageBase.prototype);
myrpc.codec.CallResponseMessage.prototype.constructor = myrpc.codec.CallResponseMessage;

myrpc.codec.CallExceptionMessage = function(name)
{
    myrpc.codec.MessageBase.call(this, myrpc.codec.MessageType.CALL_EXCEPTION);

    this._name = name;
};

myrpc.codec.CallExceptionMessage.prototype = Object.create(myrpc.codec.MessageBase.prototype);
myrpc.codec.CallExceptionMessage.prototype.constructor = myrpc.codec.CallExceptionMessage;

myrpc.codec.CallExceptionMessage.prototype.get_name = function()
{
    return this._name;
};

myrpc.codec.ErrorMessage = function(err_msg)
{
    myrpc.codec.MessageBase.call(this, myrpc.codec.MessageType.ERROR);

    this._err_msg = err_msg;
};

myrpc.codec.ErrorMessage.prototype = Object.create(myrpc.codec.MessageBase.prototype);
myrpc.codec.ErrorMessage.prototype.constructor = myrpc.codec.ErrorMessage;

myrpc.codec.ErrorMessage.prototype.get_err_msg = function()
{
    return this._err_msg;
};

myrpc.codec.CodecBase = function()
{
    myrpc.common.abstract_class(this, myrpc.codec.CodecBase);

    this._tr = null;
};

myrpc.codec.CodecBase.prototype.set_transport = function(tr)
{
    this._tr = tr;
};

myrpc.codec.CodecBase.prototype.read_message_begin = function()
{
};

myrpc.codec.CodecBase.prototype.write_message_begin = function(msg)
{
};

myrpc.codec.CodecBase.prototype.read_message_end = function()
{
};

myrpc.codec.CodecBase.prototype.write_message_end = function()
{
};

myrpc.codec.CodecBase.prototype.read_list_begin = function()
{
};

myrpc.codec.CodecBase.prototype.write_list_begin = function(llen, dtype)
{
};

myrpc.codec.CodecBase.prototype.read_list_end = function()
{
};

myrpc.codec.CodecBase.prototype.write_list_end = function()
{
};

myrpc.codec.CodecBase.prototype.read_struct_begin = function()
{
};

myrpc.codec.CodecBase.prototype.write_struct_begin = function()
{
};

myrpc.codec.CodecBase.prototype.read_struct_end = function()
{
};

myrpc.codec.CodecBase.prototype.write_struct_end = function()
{
};

myrpc.codec.CodecBase.prototype.read_field_begin = function()
{
};

myrpc.codec.CodecBase.prototype.write_field_begin = function(fid, dtype)
{
};

myrpc.codec.CodecBase.prototype.read_field_end = function()
{
};

myrpc.codec.CodecBase.prototype.write_field_end = function()
{
};

myrpc.codec.CodecBase.prototype.write_field_stop = function()
{
};

myrpc.codec.CodecBase.prototype.read_binary = function()
{
};

myrpc.codec.CodecBase.prototype.write_binary = function(buf)
{
};

myrpc.codec.CodecBase.prototype.read_string = function()
{
};

myrpc.codec.CodecBase.prototype.write_string = function(s)
{
};

myrpc.codec.CodecBase.prototype.read_bool = function()
{
};

myrpc.codec.CodecBase.prototype.write_bool = function(b)
{
};

myrpc.codec.CodecBase.prototype.read_ui8 = function()
{
};

myrpc.codec.CodecBase.prototype.write_ui8 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_ui16 = function()
{
};

myrpc.codec.CodecBase.prototype.write_ui16 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_ui32 = function()
{
};

myrpc.codec.CodecBase.prototype.write_ui32 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_ui64 = function()
{
};

myrpc.codec.CodecBase.prototype.write_ui64 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_i8 = function()
{
};

myrpc.codec.CodecBase.prototype.write_i8 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_i16 = function()
{
};

myrpc.codec.CodecBase.prototype.write_i16 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_i32 = function()
{
};

myrpc.codec.CodecBase.prototype.write_i32 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_i64 = function()
{
};

myrpc.codec.CodecBase.prototype.write_i64 = function(i)
{
};

myrpc.codec.CodecBase.prototype.read_float = function()
{
};

myrpc.codec.CodecBase.prototype.write_float = function(f)
{
};

myrpc.codec.CodecBase.prototype.read_double = function()
{
};

myrpc.codec.CodecBase.prototype.write_double = function(f)
{
};
