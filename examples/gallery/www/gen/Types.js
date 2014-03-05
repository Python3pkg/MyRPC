// THIS FILE IS AUTOMATICALLY GENERATED BY MyRPCgen 0.0.2-dev. DO NOT EDIT.

if (!("GalleryService" in window)) window.GalleryService = {};

GalleryService.Types = {};

GalleryService.Types.ImageInfo = function()
{
    this._imgid = null;
    this._thumb_width = null;
    this._thumb_height = null;
};

GalleryService.Types.ImageInfo.prototype.get_imgid = function()
{
    return this._imgid;
};

GalleryService.Types.ImageInfo.prototype.set_imgid = function(imgid)
{
    this._imgid = imgid;
};

GalleryService.Types.ImageInfo.prototype.get_thumb_width = function()
{
    return this._thumb_width;
};

GalleryService.Types.ImageInfo.prototype.set_thumb_width = function(thumb_width)
{
    this._thumb_width = thumb_width;
};

GalleryService.Types.ImageInfo.prototype.get_thumb_height = function()
{
    return this._thumb_height;
};

GalleryService.Types.ImageInfo.prototype.set_thumb_height = function(thumb_height)
{
    this._thumb_height = thumb_height;
};

GalleryService.Types.ImageInfo.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            case 0:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._imgid != null) {
                    err_dup = true;
                } else {
                    this._imgid = codec.read_ui16();
                }
                break;

            case 1:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._thumb_width != null) {
                    err_dup = true;
                } else {
                    this._thumb_width = codec.read_ui16();
                }
                break;

            case 2:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._thumb_height != null) {
                    err_dup = true;
                } else {
                    this._thumb_height = codec.read_ui16();
                }
                break;

            default:
                throw new myrpc.common.MessageBodyException("Struct ImageInfo unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct ImageInfo fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct ImageInfo fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();

    this._myrpc_validate(true);
};

GalleryService.Types.ImageInfo.prototype.myrpc_write = function(codec)
{
    this._myrpc_validate(false);

    codec.write_struct_begin();

    codec.write_field_begin(0, myrpc.codec.DataType.UI16);
    codec.write_ui16(this._imgid);
    codec.write_field_end();

    codec.write_field_begin(1, myrpc.codec.DataType.UI16);
    codec.write_ui16(this._thumb_width);
    codec.write_field_end();

    codec.write_field_begin(2, myrpc.codec.DataType.UI16);
    codec.write_ui16(this._thumb_height);
    codec.write_field_end();

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.ImageInfo.prototype._myrpc_validate = function(is_read)
{
    var msg;
    var name = null;

    if (this._imgid == null)
        name = "imgid";
    else if (this._thumb_width == null)
        name = "thumb_width";
    else if (this._thumb_height == null)
        name = "thumb_height";

    if (name != null) {
        msg = "Struct ImageInfo field " + name + " is null";

        if (is_read)
            throw new myrpc.common.MessageBodyException(msg);
        else
            throw new myrpc.common.MessageEncodeException(msg);
    }
};

GalleryService.Types.myrpc_list_read_ImageInfoList = function(codec)
{
    var linfo;
    var llen;
    var dtype;
    var i;
    var elem;
    var l = [];

    linfo = codec.read_list_begin();
    llen = linfo[0];
    dtype = linfo[1];

    if (dtype != myrpc.codec.DataType.STRUCT)
        throw new myrpc.common.MessageBodyException("List ImageInfoList has unexpected elem data type " + dtype);

    for (i = 0; i < llen; i++) {
        elem = new GalleryService.Types.ImageInfo();
        elem.myrpc_read(codec);
        l.push(elem);
    }

    codec.read_list_end();

    return l;
};

GalleryService.Types.myrpc_list_write_ImageInfoList = function(codec, l)
{
    codec.write_list_begin(l.length, myrpc.codec.DataType.STRUCT);

    l.forEach(function(elem) {
        elem.myrpc_write(codec);
    });

    codec.write_list_end();
};

GalleryService.Types.SizeTooLarge = function()
{
    this._max_width = null;
    this._max_height = null;
};

GalleryService.Types.SizeTooLarge.prototype.get_max_width = function()
{
    return this._max_width;
};

GalleryService.Types.SizeTooLarge.prototype.set_max_width = function(max_width)
{
    this._max_width = max_width;
};

GalleryService.Types.SizeTooLarge.prototype.get_max_height = function()
{
    return this._max_height;
};

GalleryService.Types.SizeTooLarge.prototype.set_max_height = function(max_height)
{
    this._max_height = max_height;
};

GalleryService.Types.SizeTooLarge.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            case 0:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._max_width != null) {
                    err_dup = true;
                } else {
                    this._max_width = codec.read_ui16();
                }
                break;

            case 1:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._max_height != null) {
                    err_dup = true;
                } else {
                    this._max_height = codec.read_ui16();
                }
                break;

            default:
                throw new myrpc.common.MessageBodyException("Struct SizeTooLarge unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct SizeTooLarge fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct SizeTooLarge fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();

    this._myrpc_validate(true);
};

GalleryService.Types.SizeTooLarge.prototype.myrpc_write = function(codec)
{
    this._myrpc_validate(false);

    codec.write_struct_begin();

    codec.write_field_begin(0, myrpc.codec.DataType.UI16);
    codec.write_ui16(this._max_width);
    codec.write_field_end();

    codec.write_field_begin(1, myrpc.codec.DataType.UI16);
    codec.write_ui16(this._max_height);
    codec.write_field_end();

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.SizeTooLarge.prototype._myrpc_validate = function(is_read)
{
    var msg;
    var name = null;

    if (this._max_width == null)
        name = "max_width";
    else if (this._max_height == null)
        name = "max_height";

    if (name != null) {
        msg = "Struct SizeTooLarge field " + name + " is null";

        if (is_read)
            throw new myrpc.common.MessageBodyException(msg);
        else
            throw new myrpc.common.MessageEncodeException(msg);
    }
};

GalleryService.Types.UnknownFormat = function()
{
};

GalleryService.Types.UnknownFormat.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            default:
                throw new myrpc.common.MessageBodyException("Struct UnknownFormat unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct UnknownFormat fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct UnknownFormat fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();
};

GalleryService.Types.UnknownFormat.prototype.myrpc_write = function(codec)
{
    codec.write_struct_begin();

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.myrpc_args_seri_list_image_info = function()
{
    this._skip_imgid = null;
};

GalleryService.Types.myrpc_args_seri_list_image_info.prototype.get_skip_imgid = function()
{
    return this._skip_imgid;
};

GalleryService.Types.myrpc_args_seri_list_image_info.prototype.set_skip_imgid = function(skip_imgid)
{
    this._skip_imgid = skip_imgid;
};

GalleryService.Types.myrpc_args_seri_list_image_info.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            case 0:
                if (dtype != myrpc.codec.DataType.UI16) {
                    err_dtype = true;
                } else if (this._skip_imgid != null) {
                    err_dup = true;
                } else {
                    this._skip_imgid = codec.read_ui16();
                }
                break;

            default:
                throw new myrpc.common.MessageBodyException("Struct args unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct args fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct args fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();
};

GalleryService.Types.myrpc_args_seri_list_image_info.prototype.myrpc_write = function(codec)
{
    codec.write_struct_begin();

    if (this._skip_imgid != null) {
        codec.write_field_begin(0, myrpc.codec.DataType.UI16);
        codec.write_ui16(this._skip_imgid);
        codec.write_field_end();
    }

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.myrpc_result_seri_list_image_info = function()
{
    this._result = null;
};

GalleryService.Types.myrpc_result_seri_list_image_info.prototype.get_result = function()
{
    return this._result;
};

GalleryService.Types.myrpc_result_seri_list_image_info.prototype.set_result = function(result)
{
    this._result = result;
};

GalleryService.Types.myrpc_result_seri_list_image_info.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            case 0:
                if (dtype != myrpc.codec.DataType.LIST) {
                    err_dtype = true;
                } else if (this._result != null) {
                    err_dup = true;
                } else {
                    this._result = GalleryService.Types.myrpc_list_read_ImageInfoList(codec);
                }
                break;

            default:
                throw new myrpc.common.MessageBodyException("Struct result unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct result fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct result fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();

    this._myrpc_validate(true);
};

GalleryService.Types.myrpc_result_seri_list_image_info.prototype.myrpc_write = function(codec)
{
    this._myrpc_validate(false);

    codec.write_struct_begin();

    codec.write_field_begin(0, myrpc.codec.DataType.LIST);
    GalleryService.Types.myrpc_list_write_ImageInfoList(codec, this._result);
    codec.write_field_end();

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.myrpc_result_seri_list_image_info.prototype._myrpc_validate = function(is_read)
{
    var msg;
    var name = null;

    if (this._result == null)
        name = "result";

    if (name != null) {
        msg = "Struct result field " + name + " is null";

        if (is_read)
            throw new myrpc.common.MessageBodyException(msg);
        else
            throw new myrpc.common.MessageEncodeException(msg);
    }
};

GalleryService.Types.myrpc_args_seri_upload_image = function()
{
    this._imgbuf = null;
};

GalleryService.Types.myrpc_args_seri_upload_image.prototype.get_imgbuf = function()
{
    return this._imgbuf;
};

GalleryService.Types.myrpc_args_seri_upload_image.prototype.set_imgbuf = function(imgbuf)
{
    this._imgbuf = imgbuf;
};

GalleryService.Types.myrpc_args_seri_upload_image.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            case 0:
                if (dtype != myrpc.codec.DataType.BINARY) {
                    err_dtype = true;
                } else if (this._imgbuf != null) {
                    err_dup = true;
                } else {
                    this._imgbuf = codec.read_binary();
                }
                break;

            default:
                throw new myrpc.common.MessageBodyException("Struct args unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct args fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct args fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();

    this._myrpc_validate(true);
};

GalleryService.Types.myrpc_args_seri_upload_image.prototype.myrpc_write = function(codec)
{
    this._myrpc_validate(false);

    codec.write_struct_begin();

    codec.write_field_begin(0, myrpc.codec.DataType.BINARY);
    codec.write_binary(this._imgbuf);
    codec.write_field_end();

    codec.write_field_stop();

    codec.write_struct_end();
};

GalleryService.Types.myrpc_args_seri_upload_image.prototype._myrpc_validate = function(is_read)
{
    var msg;
    var name = null;

    if (this._imgbuf == null)
        name = "imgbuf";

    if (name != null) {
        msg = "Struct args field " + name + " is null";

        if (is_read)
            throw new myrpc.common.MessageBodyException(msg);
        else
            throw new myrpc.common.MessageEncodeException(msg);
    }
};

GalleryService.Types.myrpc_result_seri_upload_image = function()
{
};

GalleryService.Types.myrpc_result_seri_upload_image.prototype.myrpc_read = function(codec)
{
    var finfo;
    var fid;
    var dtype;
    var err_dtype;
    var err_dup;

    codec.read_struct_begin();

    while (true) {
        finfo = codec.read_field_begin();
        fid = finfo[0];
        dtype = finfo[1];
        err_dtype = false;
        err_dup = false;

        if (fid == myrpc.codec.FID_STOP)
            break;

        switch (fid) {
            default:
                throw new myrpc.common.MessageBodyException("Struct result unknown fid " + fid);
        }

        if (err_dtype)
            throw new myrpc.common.MessageBodyException("Struct result fid " + fid + " has unexpected data type " + dtype);
        else if (err_dup)
            throw new myrpc.common.MessageBodyException("Struct result fid " + fid + " is duplicated");

        codec.read_field_end();
    }

    codec.read_struct_end();
};

GalleryService.Types.myrpc_result_seri_upload_image.prototype.myrpc_write = function(codec)
{
    codec.write_struct_begin();

    codec.write_field_stop();

    codec.write_struct_end();
};