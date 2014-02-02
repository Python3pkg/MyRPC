# FIXME: bh generation for methods -> Client.js utanahuzas
# FIXME: exc seri -> throw method, es akkor dobja ez a kivetelt (throw polimorphically...) -> Client.js utanahuzas
# FIXME: struct_read: duplicate fid handle!
# FIXME: read/write oldali exc szetvalasztas? (mashol is) -> elgondolkodas...
# FIXME: privat functionok/classname-k? (pl. _myrpc...?)
# FIXME: myrpc namespace -> error lesz belole

import re

from Constants import MYRPC_PREFIX, IDENTIFIER_RE
from GeneratorBase import GeneratorBase, StringBuilder, GeneratorException
from TypeManager import DataTypeKind
from InternalException import InternalException

_TYPES_FILENAME = "Types.js"
_CLIENT_FILENAME = "Client.js"
_ONCONTINUE = "{}{}".format(MYRPC_PREFIX, "oncontinue")
_CONTINUE = "{}{}".format(MYRPC_PREFIX, "continue")

class JSGenerator(GeneratorBase):
    """Generator for JavaScript."""

    def __init__(self, namespace, tm, methods, indent, outdir):
        super().__init__(namespace, tm, methods, indent, outdir)

        self._dtype_classp = "{}.Types".format(self._namespace)
        self._enum_read_funcp = "{}.{}enum_read".format(self._dtype_classp, MYRPC_PREFIX)
        self._enum_write_funcp = "{}.{}enum_write".format(self._dtype_classp, MYRPC_PREFIX)
        self._enum_validate_funcp = "{}.{}enum_validate".format(self._dtype_classp, MYRPC_PREFIX)
        self._list_read_funcp = "{}.{}list_read".format(self._dtype_classp, MYRPC_PREFIX)
        self._list_write_funcp = "{}.{}list_write".format(self._dtype_classp, MYRPC_PREFIX)
        self._args_seri_classp = "{}.{}args_seri".format(self._dtype_classp, MYRPC_PREFIX)
        self._result_seri_classp = "{}.{}result_seri".format(self._dtype_classp, MYRPC_PREFIX)
        self._codec_dtype_classp = "myrpc.codec.DataType"
        self._client_classn = "{}.Client".format(self._namespace)
        self._exc_handler_classp = "{}.ClientUtil.exc_handler".format(self._namespace)

        self._setup_dtype_kinds()

    def gen_types(self):
        self._open(_TYPES_FILENAME)

        self._whdr()

        self._gen_types()
        self._gen_args_result_seri()

        self._close()

    def gen_client(self):
        self._open(_CLIENT_FILENAME)

        self._whdr()

        self._gen_client()
        self._gen_exc_handler()

        self._close()

    def gen_processor(self):
        raise GeneratorException("Processor generation is not supported yet")

    @staticmethod
    def validate_ns(ns):
        for comp in ns.split("."):
            if not re.match(IDENTIFIER_RE, comp):
                raise ValueError()

    def _get_comment_prefix(self):
        return "//"

    def _gen_types(self):
        dtypes = self._sort_by_name(self._tm.list_dtype())

        for dtype in dtypes:
            s = self._gtm.gen_dtype(dtype)
            self._ws(s)

    def _gen_args_result_seri(self):
        methods = self._sort_by_name(self._methods)

        for method in methods:
            name = method.get_name()
            in_struct = method.get_in_struct()
            out_struct = method.get_out_struct()
            args_seri_classn = self._get_args_seri_classn(name)
            result_seri_classn = self._get_result_seri_classn(name)

            s = self._dtype_kind_struct_gen(in_struct, args_seri_classn)
            self._ws(s)

            s = self._dtype_kind_struct_gen(out_struct, result_seri_classn)
            self._ws(s)

    def _gen_client(self):
        sb = StringBuilder()

        sb.wl("{} = function(tr, codec)".format(self._client_classn))
        sb.wl("{")
        sb.wl("\tthis._client = new myrpc.util.ClientSubr(tr, codec);")
        sb.wl("};")
        sb.we()

        methods = self._sort_by_name(self._methods)

        for method in methods:
            name = method.get_name()
            in_struct = method.get_in_struct()
            args_seri_classn = self._get_args_seri_classn(name)
            result_seri_classn = self._get_result_seri_classn(name)
            exc_handler_classn = self._get_exc_handler_classn(name)

            in_field_names = [field.get_name() for field in in_struct.get_fields()]
            args = ["arg_{}".format(in_field_name) for in_field_name in in_field_names]

            args_oncontinue = args.copy()
            args_oncontinue.append(_ONCONTINUE)
            args_oncontinuef = ", ".join(args_oncontinue)

            sb.wl("{}.prototype.{} = function({})".format(self._client_classn, name, args_oncontinuef))
            sb.wl("{")
            sb.wl("\tvar args_seri;")
            sb.wl("\tvar result_seri;")
            sb.wl("\tvar exc_handler;")
            sb.we()

            sb.wl("\targs_seri = new {}();".format(args_seri_classn))

            for i in range(len(in_field_names)):
                in_field_name = in_field_names[i]
                arg = args[i]

                sb.wl("\targs_seri.set_{}({});".format(in_field_name, arg))

            sb.we()

            sb.wl("\tresult_seri = new {}();".format(result_seri_classn))
            sb.we()

            sb.wl("\texc_handler = new {}();".format(exc_handler_classn))
            sb.we()

            sb.wl("\tthis._client.call(\"{}\", args_seri, result_seri, exc_handler, {}, this);".format(name, _ONCONTINUE))

            sb.wl("};")
            sb.we()

        sb.wl("{}.prototype.{} = function()".format(self._client_classn, _CONTINUE))
        sb.wl("{")
        sb.wl("\tvar r = this._client.call_continue();")
        sb.we()
        sb.wl("\treturn r;")
        sb.wl("};")
        sb.we()

        self._ws(sb.get_string())

    def _gen_exc_handler(self):
        sb = StringBuilder()

        methods = self._sort_by_name(self._methods)

        for method in methods:
            name = method.get_name()
            excs = method.get_excs()
            classn = self._get_exc_handler_classn(name)

            sb.wl("{} = function()".format(classn))
            sb.wl("{")
            sb.wl("\tthis._exc = null;")
            sb.wl("};")
            sb.we()

            sb.wl("{}.prototype.read = function(codec, name)".format(classn))
            sb.wl("{")
            sb.wl("\tswitch (name) {")

            for exc in excs:
                exc_name = exc.get_name()

                sb.wl("\t\tcase \"{}\":".format(exc_name))

                s = self._gtm.read_dtype(exc, "this._exc") # FIXME
                sb.wlsindent("\t\t\t", s)

                sb.wl("\t\t\tbreak;")
                sb.we()

            sb.wl("\t\tdefault:")
            sb.wl("\t\t\tthrow new myrpc.common.MessageHeaderException(\"Unknown exception name \" + name);")
            sb.wl("\t}")
            sb.wl("};")
            sb.we()

            sb.wl("{}.prototype.throw = function()".format(classn))
            sb.wl("{")
            sb.wl("\tthrow this._exc;")
            sb.wl("};")
            sb.we()

        self._ws(sb.get_string())

    def _setup_dtype_kinds(self):
        dtype_kinds = {
            DataTypeKind.BINARY: ("BINARY", self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.STRING: ("STRING", self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.BOOL:   ("BOOL",   self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.UI8:    ("UI8",    self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.UI16:   ("UI16",   self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.UI32:   ("UI32",   self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.UI64:   ("UI64",   self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.I8:     ("I8",     self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.I16:    ("I16",    self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.I32:    ("I32",    self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.I64:    ("I64",    self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.FLOAT:  ("FLOAT",  self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.DOUBLE: ("DOUBLE", self._dtype_kind_primitive_gen, self._dtype_kind_primitive_read, self._dtype_kind_primitive_write),
            DataTypeKind.ENUM:   ("ENUM",   self._dtype_kind_enum_gen,      self._dtype_kind_enum_read,      self._dtype_kind_enum_write),
            DataTypeKind.LIST:   ("LIST",   self._dtype_kind_list_gen,      self._dtype_kind_list_read,      self._dtype_kind_list_write),
            DataTypeKind.STRUCT: ("STRUCT", self._dtype_kind_struct_gen,    self._dtype_kind_struct_read,    self._dtype_kind_struct_write),
            # Exceptions are using the same methods as structs.
            DataTypeKind.EXC:    (None,     self._dtype_kind_struct_gen,    self._dtype_kind_struct_read,    self._dtype_kind_struct_write)
        }

        self._register_dtype_kinds(dtype_kinds)

    def _dtype_kind_primitive_gen(self, dtype):
        # Primitive types don't need any generated serializer/deserializer code.

        return ""

    def _dtype_kind_primitive_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()

        sb.wl("{} = codec.read_{}();".format(v, dtype_name))

        return sb.get_string()

    def _dtype_kind_primitive_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()

        sb.wl("codec.write_{}({});".format(dtype_name, v))

        return sb.get_string()

    def _dtype_kind_enum_gen(self, dtype):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        entries = dtype.get_entries()
        values = dtype.get_values()
        classn = self._get_dtype_classn(dtype_name)
        read_funcn = self._get_enum_read_funcn(dtype_name)
        write_funcn = self._get_enum_write_funcn(dtype_name)
        validate_funcn = self._get_enum_validate_funcn(dtype_name)

        sb.wl("{} = {{".format(classn))

        lasti = len(entries) - 1

        for (i, (name, value)) in enumerate(entries):
            sb.wl("\t{}: {}{}".format(name, value, "," if i < lasti else ""))

        sb.wl("};")
        sb.we()

        sb.wl("{} = function(codec)".format(read_funcn))
        sb.wl("{")
        sb.wl("\tvar v = codec.read_i32();")
        sb.we()
        sb.wl("\t{}(true, v);".format(validate_funcn))
        sb.we()
        sb.wl("\treturn v;")
        sb.wl("};")
        sb.we()

        sb.wl("{} = function(codec, v)".format(write_funcn))
        sb.wl("{")
        sb.wl("\t{}(false, v);".format(validate_funcn))
        sb.we()
        sb.wl("\tcodec.write_i32(v);")
        sb.wl("};")
        sb.we()

        sb.wl("{} = function(is_read, v)".format(validate_funcn))
        sb.wl("{")
        sb.wl("\tvar msg;")

        valuesf = ", ".join(values)

        sb.wl("\tvar values = [{}];".format(valuesf))
        sb.we()

        sb.wl("\tif (values.indexOf(v) == -1) {")
        sb.wl("\t\tmsg = \"Enum {} unknown value \" + v;".format(dtype_name))
        sb.we()
        sb.wl("\t\tif (is_read)")
        sb.wl("\t\t\tthrow new myrpc.common.MessageDecodeException(msg);")
        sb.wl("\t\telse")
        sb.wl("\t\t\tthrow new myrpc.common.SerializeException(msg);")
        sb.wl("\t}")
        sb.wl("};")
        sb.we()

        return sb.get_string()

    def _dtype_kind_enum_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_enum_read_funcn(dtype_name)

        sb.wl("{} = {}(codec);".format(v, funcn))

        return sb.get_string()

    def _dtype_kind_enum_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_enum_write_funcn(dtype_name)

        sb.wl("{}(codec, {});".format(funcn, v))

        return sb.get_string()

    def _dtype_kind_list_gen(self, dtype):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        elem_dtype = dtype.get_elem_dtype()
        read_funcn = self._get_list_read_funcn(dtype_name)
        write_funcn = self._get_list_write_funcn(dtype_name)
        codec_dtype_classn = self._get_codec_dtype_classn(elem_dtype)

        sb.wl("{} = function(codec)".format(read_funcn))
        sb.wl("{")
        sb.wl("\tvar linfo;")
        sb.wl("\tvar llen;")
        sb.wl("\tvar dtype;")
        sb.wl("\tvar i;")
        sb.wl("\tvar elem;")
        sb.wl("\tvar l = [];")
        sb.we()
        sb.wl("\tlinfo = codec.read_list_begin();")
        sb.wl("\tllen = linfo[0];")
        sb.wl("\tdtype = linfo[1];")
        sb.we()
        sb.wl("\tif (dtype != {})".format(codec_dtype_classn))
        sb.wl("\t\tthrow new myrpc.common.MessageDecodeException(\"List {} has unexpected elem data type \" + dtype);".format(dtype_name))
        sb.we()
        sb.wl("\tfor (i = 0; i < llen; i++) {")

        s = self._gtm.read_dtype(elem_dtype, "elem")
        sb.wlsindent("\t\t", s)

        sb.wl("\t\tl.push(elem);")
        sb.wl("\t}")
        sb.we()
        sb.wl("\tcodec.read_list_end();")
        sb.we()
        sb.wl("\treturn l;")
        sb.wl("};")
        sb.we()

        sb.wl("{} = function(codec, l)".format(write_funcn))
        sb.wl("{")
        sb.wl("\tcodec.write_list_begin(l.length, {});".format(codec_dtype_classn))
        sb.we()
        sb.wl("\tl.foreach(function(elem) {")

        s = self._gtm.write_dtype(elem_dtype, "elem")
        sb.wlsindent("\t\t", s)

        sb.wl("\t});")
        sb.we()
        sb.wl("\tcodec.write_list_end();")
        sb.wl("};")
        sb.we()

        return sb.get_string()

    def _dtype_kind_list_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_list_read_funcn(dtype_name)

        sb.wl("{} = {}(codec);".format(v, funcn))

        return sb.get_string()

    def _dtype_kind_list_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_list_write_funcn(dtype_name)

        sb.wl("{}(codec, {});".format(funcn, v))

        return sb.get_string()

    def _dtype_kind_struct_gen(self, dtype, classn = None):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        fields = dtype.get_fields()

        # We have the option to override classname, it is used
        # during method args_seri/result_seri generation (these are
        # structs).

        if classn == None:
            classn = self._get_dtype_classn(dtype_name)

        # Do we need to generate validation method?

        is_validate_needed = False
        for field in fields:
            if field.get_req():
                is_validate_needed = True
                break

        sb.wl("{} = function()".format(classn))
        sb.wl("{")

        for field in fields:
            name = field.get_name()

            sb.wl("\tthis._{} = null;".format(name))

        sb.wl("};")
        sb.we()

        # The generated code uses setters/getters to avoid problems
        # regarding instance variable <-> method name overlap.

        for field in fields:
            name = field.get_name()

            sb.wl("{}.prototype.get_{} = function()".format(classn, name))
            sb.wl("{")
            sb.wl("\treturn this._{};".format(name))
            sb.wl("};")
            sb.we()

            sb.wl("{0}.prototype.set_{1} = function({1})".format(classn, name))
            sb.wl("{")
            sb.wl("\tthis._{0} = {0};".format(name))
            sb.wl("};")
            sb.we()

        sb.wl("{}.prototype.read = function(codec)".format(classn))
        sb.wl("{")
        sb.wl("\tvar finfo;")
        sb.wl("\tvar fid;")
        sb.wl("\tvar dtype;")
        sb.wl("\tvar err;")
        sb.we()
        sb.wl("\tcodec.read_struct_begin();")
        sb.we()
        sb.wl("\twhile (true) {")
        sb.wl("\t\tfinfo = codec.read_field_begin();")
        sb.wl("\t\tfid = finfo[0];")
        sb.wl("\t\tdtype = finfo[1];")
        sb.wl("\t\terr = false;")
        sb.we()
        sb.wl("\t\tif (fid == myrpc.codec.FID_STOP)")
        sb.wl("\t\t\tbreak;")
        sb.we()
        sb.wl("\t\tswitch (fid) {")

        for field in fields:
            fid = field.get_fid()
            field_dtype = field.get_dtype()
            name = field.get_name()
            codec_dtype_classn = self._get_codec_dtype_classn(field_dtype)

            sb.wl("\t\t\tcase {}:".format(fid))
            sb.wl("\t\t\t\tif (dtype == {}) {{".format(codec_dtype_classn))

            s = self._gtm.read_dtype(field_dtype, "this._{}".format(name))
            sb.wlsindent("\t\t\t\t\t", s)

            sb.wl("\t\t\t\t} else {")
            sb.wl("\t\t\t\t\terr = true;")
            sb.wl("\t\t\t\t}")

            sb.wl("\t\t\t\tbreak;")
            sb.we()

        sb.wl("\t\t\tdefault:")
        sb.wl("\t\t\t\tthrow new myrpc.common.MessageDecodeException(\"Struct {} unknown fid \" + fid);".format(dtype_name))
        sb.wl("\t\t}")
        sb.we()
        sb.wl("\t\tif (err)")
        sb.wl("\t\t\tthrow new myrpc.common.MessageDecodeException(\"Struct {} fid \" + fid + \" has unexpected data type \" + dtype);".format(dtype_name))
        sb.we()
        sb.wl("\t\tcodec.read_field_end();")
        sb.wl("\t}")
        sb.we()
        sb.wl("\tcodec.read_struct_end();")

        if is_validate_needed:
            sb.we()
            sb.wl("\tthis._validate(true);")

        sb.wl("};")
        sb.we()

        sb.wl("{}.prototype.write = function(codec)".format(classn))
        sb.wl("{")

        if is_validate_needed:
            sb.wl("\tthis._validate(false);")
            sb.we()

        sb.wl("\tcodec.write_struct_begin();")
        sb.we()

        for field in fields:
            fid = field.get_fid()
            req = field.get_req()
            field_dtype = field.get_dtype()
            name = field.get_name()
            codec_dtype_classn = self._get_codec_dtype_classn(field_dtype)

            indent = "\t"

            if not req:
                sb.wl("\tif (this._{} != null) {{".format(name))
                indent += "\t"

            sb.wl("{}codec.write_field_begin({}, {});".format(indent, fid, codec_dtype_classn))

            s = self._gtm.write_dtype(field_dtype, "this._{}".format(name))
            sb.wlsindent(indent, s)

            sb.wl("{}codec.write_field_end();".format(indent))

            if not req:
                sb.wl("\t}")

            sb.we()

        sb.wl("\tcodec.write_field_stop();")
        sb.we()
        sb.wl("\tcodec.write_struct_end();")
        sb.wl("};")
        sb.we()

        if is_validate_needed:
            sb.wl("{}.prototype._validate = function(is_read)".format(classn))
            sb.wl("{")
            sb.wl("\tvar msg;")
            sb.wl("\tvar name = null;")
            sb.we()

            for (i, field) in enumerate(fields):
                req = field.get_req()
                name = field.get_name()

                if req:
                    sb.wl("\t{} (this._{} == null)".format("else if" if i > 0 else "if", name))
                    sb.wl("\t\tname = \"{}\";".format(name))

            sb.we()
            sb.wl("\tif (name != null) {")
            sb.wl("\t\tmsg = \"Struct {} field \" + name + \" is null\";".format(dtype_name))
            sb.we()
            sb.wl("\t\tif (is_read)")
            sb.wl("\t\t\tthrow new myrpc.common.MessageDecodeException(msg);")
            sb.wl("\t\telse")
            sb.wl("\t\t\tthrow new myrpc.common.SerializeException(msg);")
            sb.wl("\t}")

            sb.wl("};")
            sb.we()

        return sb.get_string()

    def _dtype_kind_struct_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        classn = self._get_dtype_classn(dtype_name)

        sb.wl("{} = new {}();".format(v, classn))
        sb.wl("{}.read(codec);".format(v))

        return sb.get_string()

    def _dtype_kind_struct_write(self, dtype, v):
        sb = StringBuilder()

        sb.wl("{}.write(codec);".format(v))

        return sb.get_string()

    def _get_dtype_classn(self, name):
        classn = "{}.{}".format(self._dtype_classp, name)

        return classn

    def _get_enum_read_funcn(self, name):
        funcn = "{}_{}".format(self._enum_read_funcp, name)

        return funcn

    def _get_enum_write_funcn(self, name):
        funcn = "{}_{}".format(self._enum_write_funcp, name)

        return funcn

    def _get_enum_validate_funcn(self, name):
        funcn = "{}_{}".format(self._enum_validate_funcp, name)

        return funcn

    def _get_list_read_funcn(self, name):
        funcn = "{}_{}".format(self._list_read_funcp, name)

        return funcn

    def _get_list_write_funcn(self, name):
        funcn = "{}_{}".format(self._list_write_funcp, name)

        return funcn

    def _get_args_seri_classn(self, name):
        classn = "{}_{}".format(self._args_seri_classp, name)

        return classn

    def _get_result_seri_classn(self, name):
        classn = "{}_{}".format(self._result_seri_classp, name)

        return classn

    def _get_codec_dtype_classn(self, dtype):
        codec_dtype = self._gtm.get_codec_dtype(dtype)
        if codec_dtype == None:
            raise InternalException("codec_dtype is None")

        classn = "{}.{}".format(self._codec_dtype_classp, codec_dtype)

        return classn

    def _get_exc_handler_classn(self, name):
        classn = "{}_{}".format(self._exc_handler_classp, name)

        return classn

GeneratorBase.register_gen("js", JSGenerator)
