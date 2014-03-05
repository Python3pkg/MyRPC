# THIS FILE IS AUTOMATICALLY GENERATED BY MyRPCgen 0.0.2-dev. DO NOT EDIT.

import myrpc.Common
import myrpc.codec.CodecBase

class ImageInfo:
    def __init__(self):
        self._imgid = None
        self._thumb_width = None
        self._thumb_height = None

    def get_imgid(self):
        return self._imgid

    def set_imgid(self, imgid):
        self._imgid = imgid

    def get_thumb_width(self):
        return self._thumb_width

    def set_thumb_width(self, thumb_width):
        self._thumb_width = thumb_width

    def get_thumb_height(self):
        return self._thumb_height

    def set_thumb_height(self, thumb_height):
        self._thumb_height = thumb_height

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            if fid == 0:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._imgid != None:
                    err_dup = True
                else:
                    self._imgid = codec.read_ui16()
            elif fid == 1:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._thumb_width != None:
                    err_dup = True
                else:
                    self._thumb_width = codec.read_ui16()
            elif fid == 2:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._thumb_height != None:
                    err_dup = True
                else:
                    self._thumb_height = codec.read_ui16()
            else:
                raise myrpc.Common.MessageBodyException("Struct ImageInfo unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct ImageInfo fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct ImageInfo fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

        self._myrpc_validate(True)

    def myrpc_write(self, codec):
        self._myrpc_validate(False)

        codec.write_struct_begin()

        codec.write_field_begin(0, myrpc.codec.CodecBase.DataType.UI16)
        codec.write_ui16(self._imgid)
        codec.write_field_end()

        codec.write_field_begin(1, myrpc.codec.CodecBase.DataType.UI16)
        codec.write_ui16(self._thumb_width)
        codec.write_field_end()

        codec.write_field_begin(2, myrpc.codec.CodecBase.DataType.UI16)
        codec.write_ui16(self._thumb_height)
        codec.write_field_end()

        codec.write_field_stop()

        codec.write_struct_end()

    def _myrpc_validate(self, is_read):
        name = None

        if self._imgid == None:
            name = "imgid"
        elif self._thumb_width == None:
            name = "thumb_width"
        elif self._thumb_height == None:
            name = "thumb_height"

        if name != None:
            msg = "Struct ImageInfo field {} is None".format(name)

            if is_read:
                raise myrpc.Common.MessageBodyException(msg)
            else:
                raise myrpc.Common.MessageEncodeException(msg)

def myrpc_list_read_ImageInfoList(codec):
    (llen, dtype) = codec.read_list_begin()

    if dtype != myrpc.codec.CodecBase.DataType.STRUCT:
        raise myrpc.Common.MessageBodyException("List ImageInfoList has unexpected elem data type {}".format(dtype))

    l = []

    for i in range(llen):
        elem = ImageInfo()
        elem.myrpc_read(codec)
        l.append(elem)

    codec.read_list_end()

    return l

def myrpc_list_write_ImageInfoList(codec, l):
    codec.write_list_begin(len(l), myrpc.codec.CodecBase.DataType.STRUCT)

    for elem in l:
        elem.myrpc_write(codec)

    codec.write_list_end()

class SizeTooLarge(Exception):
    def __init__(self):
        super().__init__()

        self._max_width = None
        self._max_height = None

    def get_max_width(self):
        return self._max_width

    def set_max_width(self, max_width):
        self._max_width = max_width

    def get_max_height(self):
        return self._max_height

    def set_max_height(self, max_height):
        self._max_height = max_height

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            if fid == 0:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._max_width != None:
                    err_dup = True
                else:
                    self._max_width = codec.read_ui16()
            elif fid == 1:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._max_height != None:
                    err_dup = True
                else:
                    self._max_height = codec.read_ui16()
            else:
                raise myrpc.Common.MessageBodyException("Struct SizeTooLarge unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct SizeTooLarge fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct SizeTooLarge fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

        self._myrpc_validate(True)

    def myrpc_write(self, codec):
        self._myrpc_validate(False)

        codec.write_struct_begin()

        codec.write_field_begin(0, myrpc.codec.CodecBase.DataType.UI16)
        codec.write_ui16(self._max_width)
        codec.write_field_end()

        codec.write_field_begin(1, myrpc.codec.CodecBase.DataType.UI16)
        codec.write_ui16(self._max_height)
        codec.write_field_end()

        codec.write_field_stop()

        codec.write_struct_end()

    def _myrpc_validate(self, is_read):
        name = None

        if self._max_width == None:
            name = "max_width"
        elif self._max_height == None:
            name = "max_height"

        if name != None:
            msg = "Struct SizeTooLarge field {} is None".format(name)

            if is_read:
                raise myrpc.Common.MessageBodyException(msg)
            else:
                raise myrpc.Common.MessageEncodeException(msg)

class UnknownFormat(Exception):
    def __init__(self):
        super().__init__()

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            raise myrpc.Common.MessageBodyException("Struct UnknownFormat unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct UnknownFormat fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct UnknownFormat fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

    def myrpc_write(self, codec):
        codec.write_struct_begin()

        codec.write_field_stop()

        codec.write_struct_end()

class myrpc_args_seri_list_image_info:
    def __init__(self):
        self._skip_imgid = None

    def get_skip_imgid(self):
        return self._skip_imgid

    def set_skip_imgid(self, skip_imgid):
        self._skip_imgid = skip_imgid

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            if fid == 0:
                if dtype != myrpc.codec.CodecBase.DataType.UI16:
                    err_dtype = True
                elif self._skip_imgid != None:
                    err_dup = True
                else:
                    self._skip_imgid = codec.read_ui16()
            else:
                raise myrpc.Common.MessageBodyException("Struct args unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct args fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct args fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

    def myrpc_write(self, codec):
        codec.write_struct_begin()

        if self._skip_imgid != None:
            codec.write_field_begin(0, myrpc.codec.CodecBase.DataType.UI16)
            codec.write_ui16(self._skip_imgid)
            codec.write_field_end()

        codec.write_field_stop()

        codec.write_struct_end()

class myrpc_result_seri_list_image_info:
    def __init__(self):
        self._result = None

    def get_result(self):
        return self._result

    def set_result(self, result):
        self._result = result

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            if fid == 0:
                if dtype != myrpc.codec.CodecBase.DataType.LIST:
                    err_dtype = True
                elif self._result != None:
                    err_dup = True
                else:
                    self._result = myrpc_list_read_ImageInfoList(codec)
            else:
                raise myrpc.Common.MessageBodyException("Struct result unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct result fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct result fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

        self._myrpc_validate(True)

    def myrpc_write(self, codec):
        self._myrpc_validate(False)

        codec.write_struct_begin()

        codec.write_field_begin(0, myrpc.codec.CodecBase.DataType.LIST)
        myrpc_list_write_ImageInfoList(codec, self._result)
        codec.write_field_end()

        codec.write_field_stop()

        codec.write_struct_end()

    def _myrpc_validate(self, is_read):
        name = None

        if self._result == None:
            name = "result"

        if name != None:
            msg = "Struct result field {} is None".format(name)

            if is_read:
                raise myrpc.Common.MessageBodyException(msg)
            else:
                raise myrpc.Common.MessageEncodeException(msg)

class myrpc_args_seri_upload_image:
    def __init__(self):
        self._imgbuf = None

    def get_imgbuf(self):
        return self._imgbuf

    def set_imgbuf(self, imgbuf):
        self._imgbuf = imgbuf

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            if fid == 0:
                if dtype != myrpc.codec.CodecBase.DataType.BINARY:
                    err_dtype = True
                elif self._imgbuf != None:
                    err_dup = True
                else:
                    self._imgbuf = codec.read_binary()
            else:
                raise myrpc.Common.MessageBodyException("Struct args unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct args fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct args fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

        self._myrpc_validate(True)

    def myrpc_write(self, codec):
        self._myrpc_validate(False)

        codec.write_struct_begin()

        codec.write_field_begin(0, myrpc.codec.CodecBase.DataType.BINARY)
        codec.write_binary(self._imgbuf)
        codec.write_field_end()

        codec.write_field_stop()

        codec.write_struct_end()

    def _myrpc_validate(self, is_read):
        name = None

        if self._imgbuf == None:
            name = "imgbuf"

        if name != None:
            msg = "Struct args field {} is None".format(name)

            if is_read:
                raise myrpc.Common.MessageBodyException(msg)
            else:
                raise myrpc.Common.MessageEncodeException(msg)

class myrpc_result_seri_upload_image:
    def __init__(self):
        pass

    def myrpc_read(self, codec):
        codec.read_struct_begin()

        while True:
            (fid, dtype) = codec.read_field_begin()
            err_dtype = False
            err_dup = False

            if fid == myrpc.codec.CodecBase.FID_STOP:
                break

            raise myrpc.Common.MessageBodyException("Struct result unknown fid {}".format(fid))

            if err_dtype:
                raise myrpc.Common.MessageBodyException("Struct result fid {} has unexpected data type {}".format(fid, dtype))
            elif err_dup:
                raise myrpc.Common.MessageBodyException("Struct result fid {} is duplicated".format(fid))

            codec.read_field_end()

        codec.read_struct_end()

    def myrpc_write(self, codec):
        codec.write_struct_begin()

        codec.write_field_stop()

        codec.write_struct_end()