import os
import os.path
import re

from Constants import MYRPC_PREFIX, U_MYRPC_PREFIX, ENCODING, IDENTIFIER_RE, RESULT_FIELD_NAME
from GeneratorBase import StructFieldAccess, GeneratorBase, StringBuilder, GeneratorException
from TypeManager import DataTypeKind
from InternalException import InternalException

_INIT_FILENAME = "__init__.py"
_TYPES_MODULE = "Types"
_TYPES_FILENAME = "{}.py".format(_TYPES_MODULE)
_PROCESSOR_FILENAME = "Processor.py"
_ARGS_RESULT_SERI_SFA = StructFieldAccess.UNDERSCORE
_STRUCT_READ = "{}read".format(MYRPC_PREFIX)
_STRUCT_WRITE = "{}write".format(MYRPC_PREFIX)
_STRUCT_VALIDATE = "{}validate".format(U_MYRPC_PREFIX)
_NS_SEPARATOR = "."

class PyGenerator(GeneratorBase):
    """Generator for Python."""

    def __init__(self, namespace, tm, methods, indent, sfa, outdir):
        super().__init__(namespace, tm, methods, indent, sfa, outdir)

        self._enum_read_funcp = "{}enum_read".format(MYRPC_PREFIX)
        self._enum_write_funcp = "{}enum_write".format(MYRPC_PREFIX)
        self._enum_validate_funcp = "{}enum_validate".format(MYRPC_PREFIX)
        self._list_read_funcp = "{}list_read".format(MYRPC_PREFIX)
        self._list_write_funcp = "{}list_write".format(MYRPC_PREFIX)
        self._args_seri_classp = "{}args_seri".format(MYRPC_PREFIX)
        self._result_seri_classp = "{}result_seri".format(MYRPC_PREFIX)
        self._codec_dtype_classp = "myrpc.codec.CodecBase.DataType"

        self._setup_dtype_kinds()

    def create_outdir(self):
        # Create Python package subdirectories according to namespace.

        compl = self._namespace.split(_NS_SEPARATOR)

        for i in range(len(compl) + 1):
            dirname = os.path.join(self._outdir, *compl[:i])

            try:
                os.mkdir(dirname)
            except FileExistsError:
                pass
            except OSError as e:
                raise GeneratorException(e)

            if i > 0:
                try:
                    filename = os.path.join(dirname, _INIT_FILENAME)
                    f = open(filename, mode = "xt", encoding = ENCODING)
                    f.close()
                except OSError as e:
                    raise GeneratorException(e)

        self._outdir = dirname # FIXME: create new variable?

    def gen_types(self):
        self._open(_TYPES_FILENAME)

        self._whdr()

        # Do not use from ... import ... statement here, since it can
        # lead to IDL type conflict.

        sb = StringBuilder()
        sb.wl("import myrpc.Common")
        sb.wl("import myrpc.codec.CodecBase")
        sb.we()
        self._ws(sb.get_string())

        self._gen_types()
        self._gen_args_result_seri()

        self._close()

    def gen_client(self):
        raise GeneratorException("Client generation is not supported yet")

    def gen_processor(self):
        self._open(_PROCESSOR_FILENAME)

        self._whdr()

        # Use Types. prefix to reference the types in Types module (to
        # prevent IDL type conflict).

        sb = StringBuilder()
        sb.wl("from abc import ABCMeta, abstractmethod")
        sb.we()
        sb.wl("from myrpc.util.ProcessorSubr import HandlerReturn, ProcessorSubr")
        sb.wl("from {} import {}".format(self._namespace, _TYPES_MODULE))
        sb.we()
        self._ws(sb.get_string())

        self._gen_iface()
        self._gen_processor()

        self._close()

    @staticmethod
    def validate_ns(ns):
        for comp in ns.split(_NS_SEPARATOR):
            if not re.match(IDENTIFIER_RE, comp):
                raise ValueError()

    def _get_comment_prefix(self):
        return "#"

    def _get_var_prefix(self):
        return "self"

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

            # Use fixed sfa during method args/result seri generation, because
            # setter/getter naming can have dependencies in client/processor subrs.

            s = self._dtype_kind_struct_gen(in_struct, args_seri_classn, _ARGS_RESULT_SERI_SFA)
            self._ws(s)

            s = self._dtype_kind_struct_gen(out_struct, result_seri_classn, _ARGS_RESULT_SERI_SFA)
            self._ws(s)

    def _gen_iface(self):
        sb = StringBuilder()

        sb.wl("class Interface(metaclass = ABCMeta):")

        methods = self._sort_by_name(self._methods)

        if len(methods) == 0:
            sb.wl("\tpass")
            sb.we()
        else:
            for method in methods:
                name = method.get_name()
                in_struct = method.get_in_struct()

                args = [field.get_name() for field in in_struct.get_fields()]
                args.insert(0, "self")
                argsf = ", ".join(args)

                sb.wl("\t@abstractmethod")
                sb.wl("\tdef {}({}):".format(name, argsf))
                sb.wl("\t\tpass")
                sb.we()

        self._ws(sb.get_string())

    def _gen_processor(self):
        sb = StringBuilder()

        classn_prefix = "{}.".format(_TYPES_MODULE)

        methods = self._sort_by_name(self._methods)

        sb.wl("class Processor:")
        sb.wl("\tdef __init__(self, impl):")
        sb.wl("\t\tself._impl = impl")
        sb.we()

        sb.wl("\t\tmethodmap = {")

        lasti = len(methods) - 1

        for (i, method) in enumerate(methods):
            name = method.get_name()
            args_seri_classn = self._get_args_seri_classn(name, classn_prefix)

            sb.wl("\t\t\t\"{0}\": ({1}, self._handle_{0}){2}".format(name, args_seri_classn, "," if i < lasti else ""))

        sb.wl("\t\t}")
        sb.we()

        sb.wl("\t\tself._proc = ProcessorSubr(methodmap)")
        sb.we()

        sb.wl("\tdef process_one(self, tr, codec):")
        sb.wl("\t\tself._proc.process_one(tr, codec)")
        sb.we()

        for method in methods:
            name = method.get_name()
            in_struct = method.get_in_struct()
            excs = method.get_excs()
            has_result = method.has_result()
            result_seri_classn = self._get_result_seri_classn(name, classn_prefix)

            sb.wl("\tdef _handle_{}(self, args_seri):".format(name))

            in_field_names = [field.get_name() for field in in_struct.get_fields()]
            args = ["arg_{}".format(in_field_name) for in_field_name in in_field_names]
            argsf = ", ".join(args)

            for i in range(len(in_field_names)):
                in_field_name = in_field_names[i]
                arg = args[i]
                getter_invoke = self._get_struct_field_getter_invoke("args_seri", in_field_name, arg, _ARGS_RESULT_SERI_SFA)

                sb.wl("\t\t{}".format(getter_invoke))

            if len(in_field_names) > 0:
                sb.we()

            sb.wl("\t\texc_name = None")
            sb.we()

            indent = "\t\t"

            if len(excs) > 0:
                sb.wl("\t\ttry:")
                indent += "\t"

            sb.wl("{}{}self._impl.{}({})".format(indent, "r = " if has_result else "", name, argsf))

            for exc in excs:
                exc_name = exc.get_name()
                exc_classn = self._get_dtype_classn(exc_name, classn_prefix)

                sb.wl("\t\texcept {} as e:".format(exc_classn))
                sb.wl("\t\t\texc_name = \"{}\"".format(exc_name))
                sb.wl("\t\t\texc = e")

            sb.we()
            sb.wl("\t\thr = HandlerReturn()")
            sb.we()

            sb.wl("\t\tif exc_name != None:")
            sb.wl("\t\t\thr.set_exc(exc, exc_name)")
            sb.wl("\t\telse:")
            sb.wl("\t\t\tresult_seri = {}()".format(result_seri_classn))

            if has_result:
                setter_invoke = self._get_struct_field_setter_invoke("result_seri", RESULT_FIELD_NAME, "r", _ARGS_RESULT_SERI_SFA)
                sb.wl("\t\t\t{}".format(setter_invoke))

            sb.we()
            sb.wl("\t\t\thr.set_result(result_seri)")
            sb.we()
            sb.wl("\t\treturn hr")
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

        sb.wl("{} = codec.read_{}()".format(v, dtype_name))

        return sb.get_string()

    def _dtype_kind_primitive_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()

        sb.wl("codec.write_{}({})".format(dtype_name, v))

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

        sb.wl("class {}:".format(classn))

        if len(entries) == 0:
            sb.wl("\tpass")
        else:
            for (name, value) in entries:
                sb.wl("\t{} = {}".format(name, value))

        sb.we()

        sb.wl("def {}(codec):".format(read_funcn))
        sb.wl("\tv = codec.read_i32()")
        sb.we()
        sb.wl("\t{}(True, v)".format(validate_funcn))
        sb.we()
        sb.wl("\treturn v")
        sb.we()

        sb.wl("def {}(codec, v):".format(write_funcn))
        sb.wl("\t{}(False, v)".format(validate_funcn))
        sb.we()
        sb.wl("\tcodec.write_i32(v)")
        sb.we()

        sb.wl("def {}(is_read, v):".format(validate_funcn))

        valuesf = ", ".join(values)
        if len(values) == 1:
            valuesf += ","

        sb.wl("\tvalues = ({})".format(valuesf))
        sb.we()

        sb.wl("\tif v not in values:")
        sb.wl("\t\tmsg = \"Enum {} unknown value {{}}\".format(v)".format(dtype_name))
        sb.we()
        sb.wl("\t\tif is_read:")
        sb.wl("\t\t\traise myrpc.Common.MessageBodyException(msg)")
        sb.wl("\t\telse:")
        sb.wl("\t\t\traise myrpc.Common.MessageEncodeException(msg)")
        sb.we()

        return sb.get_string()

    def _dtype_kind_enum_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_enum_read_funcn(dtype_name)

        sb.wl("{} = {}(codec)".format(v, funcn))

        return sb.get_string()

    def _dtype_kind_enum_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_enum_write_funcn(dtype_name)

        sb.wl("{}(codec, {})".format(funcn, v))

        return sb.get_string()

    def _dtype_kind_list_gen(self, dtype):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        elem_dtype = dtype.get_elem_dtype()
        read_funcn = self._get_list_read_funcn(dtype_name)
        write_funcn = self._get_list_write_funcn(dtype_name)
        codec_dtype_classn = self._get_codec_dtype_classn(elem_dtype)

        sb.wl("def {}(codec):".format(read_funcn))
        sb.wl("\t(llen, dtype) = codec.read_list_begin()")
        sb.we()
        sb.wl("\tif dtype != {}:".format(codec_dtype_classn))
        sb.wl("\t\traise myrpc.Common.MessageBodyException(\"List {} has unexpected elem data type {{}}\".format(dtype))".format(dtype_name))
        sb.we()
        sb.wl("\tl = []")
        sb.we()
        sb.wl("\tfor i in range(llen):")

        s = self._gtm.read_dtype(elem_dtype, "elem")
        sb.wlsindent("\t\t", s)

        sb.wl("\t\tl.append(elem)")
        sb.we()
        sb.wl("\tcodec.read_list_end()")
        sb.we()
        sb.wl("\treturn l")
        sb.we()

        sb.wl("def {}(codec, l):".format(write_funcn))
        sb.wl("\tcodec.write_list_begin(len(l), {})".format(codec_dtype_classn))
        sb.we()
        sb.wl("\tfor elem in l:")

        s = self._gtm.write_dtype(elem_dtype, "elem")
        sb.wlsindent("\t\t", s)

        sb.we()
        sb.wl("\tcodec.write_list_end()")
        sb.we()

        return sb.get_string()

    def _dtype_kind_list_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_list_read_funcn(dtype_name)

        sb.wl("{} = {}(codec)".format(v, funcn))

        return sb.get_string()

    def _dtype_kind_list_write(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        funcn = self._get_list_write_funcn(dtype_name)

        sb.wl("{}(codec, {})".format(funcn, v))

        return sb.get_string()

    def _dtype_kind_struct_gen(self, dtype, classn = None, sfa = None):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        fields = dtype.get_fields()
        dtype_kind_is_exc = (dtype.get_dtype_kind() == DataTypeKind.EXC)

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

        if sfa == None:
            sfa = self._sfa

        parent_classn = "(Exception)" if dtype_kind_is_exc else ""
        sb.wl("class {}{}:".format(classn, parent_classn))

        sb.wl("\tdef __init__(self):")

        if dtype_kind_is_exc:
            sb.wl("\t\tsuper().__init__()")
            if len(fields) > 0:
                sb.we()
        elif len(fields) == 0:
            sb.wl("\t\tpass")

        for field in fields:
            name = field.get_name()
            var_name = self._get_struct_field_var_name(name, sfa)

            sb.wl("\t\t{} = None".format(var_name))

        sb.we()

        # Generate setter/getter methods.

        self._sfa_check_start(dtype_name)

        for field in fields:
            name = field.get_name()
            var_name = self._get_struct_field_var_name(name, sfa)
            getter_name = self._get_struct_field_getter_name(name, sfa)
            setter_name = self._get_struct_field_setter_name(name, sfa)

            if getter_name != None:
                self._sfa_check_name(getter_name)

                sb.wl("\tdef {}(self):".format(getter_name))
                sb.wl("\t\treturn {}".format(var_name))
                sb.we()

            if setter_name != None:
                self._sfa_check_name(setter_name)

                sb.wl("\tdef {}(self, {}):".format(setter_name, name))
                sb.wl("\t\t{} = {}".format(var_name, name))
                sb.we()

        # Generate serializer, deserializer and validator methods.

        sb.wl("\tdef {}(self, codec):".format(_STRUCT_READ))
        sb.wl("\t\tcodec.read_struct_begin()")
        sb.we()
        sb.wl("\t\twhile True:")
        sb.wl("\t\t\t(fid, dtype) = codec.read_field_begin()")
        sb.wl("\t\t\terr_dtype = False")
        sb.wl("\t\t\terr_dup = False")
        sb.we()
        sb.wl("\t\t\tif fid == myrpc.codec.CodecBase.FID_STOP:")
        sb.wl("\t\t\t\tbreak")
        sb.we()

        for (i, field) in enumerate(fields):
            fid = field.get_fid()
            field_dtype = field.get_dtype()
            name = field.get_name()
            var_name = self._get_struct_field_var_name(name, sfa)
            codec_dtype_classn = self._get_codec_dtype_classn(field_dtype)

            sb.wl("\t\t\t{} fid == {}:".format("elif" if i > 0 else "if", fid))
            sb.wl("\t\t\t\tif dtype != {}:".format(codec_dtype_classn))
            sb.wl("\t\t\t\t\terr_dtype = True")
            sb.wl("\t\t\t\telif {} != None:".format(var_name))
            sb.wl("\t\t\t\t\terr_dup = True")
            sb.wl("\t\t\t\telse:")

            s = self._gtm.read_dtype(field_dtype, var_name)
            sb.wlsindent("\t\t\t\t\t", s)

        indent = "\t\t\t"

        if len(fields) > 0:
            sb.wl("\t\t\telse:")
            indent += "\t"

        sb.wl("{}raise myrpc.Common.MessageBodyException(\"Struct {} unknown fid {{}}\".format(fid))".format(indent, dtype_name))

        sb.we()
        sb.wl("\t\t\tif err_dtype:")
        sb.wl("\t\t\t\traise myrpc.Common.MessageBodyException(\"Struct {} fid {{}} has unexpected data type {{}}\".format(fid, dtype))".format(dtype_name))
        sb.wl("\t\t\telif err_dup:")
        sb.wl("\t\t\t\traise myrpc.Common.MessageBodyException(\"Struct {} fid {{}} is duplicated\".format(fid))".format(dtype_name))
        sb.we()
        sb.wl("\t\t\tcodec.read_field_end()")
        sb.we()
        sb.wl("\t\tcodec.read_struct_end()")

        if is_validate_needed:
            sb.we()
            sb.wl("\t\tself.{}(True)".format(_STRUCT_VALIDATE))

        sb.we()

        sb.wl("\tdef {}(self, codec):".format(_STRUCT_WRITE))

        if is_validate_needed:
            sb.wl("\t\tself.{}(False)".format(_STRUCT_VALIDATE))
            sb.we()

        sb.wl("\t\tcodec.write_struct_begin()")
        sb.we()

        for field in fields:
            fid = field.get_fid()
            req = field.get_req()
            field_dtype = field.get_dtype()
            name = field.get_name()
            var_name = self._get_struct_field_var_name(name, sfa)
            codec_dtype_classn = self._get_codec_dtype_classn(field_dtype)

            indent = "\t\t"

            if not req:
                sb.wl("\t\tif {} != None:".format(var_name))
                indent += "\t"

            sb.wl("{}codec.write_field_begin({}, {})".format(indent, fid, codec_dtype_classn))

            s = self._gtm.write_dtype(field_dtype, var_name)
            sb.wlsindent(indent, s)

            sb.wl("{}codec.write_field_end()".format(indent))
            sb.we()

        sb.wl("\t\tcodec.write_field_stop()")
        sb.we()
        sb.wl("\t\tcodec.write_struct_end()")
        sb.we()

        if is_validate_needed:
            sb.wl("\tdef {}(self, is_read):".format(_STRUCT_VALIDATE))
            sb.wl("\t\tname = None")
            sb.we()

            i = 0

            for field in fields:
                req = field.get_req()
                name = field.get_name()
                var_name = self._get_struct_field_var_name(name, sfa)

                if req:
                    sb.wl("\t\t{} {} == None:".format("elif" if i > 0 else "if", var_name))
                    sb.wl("\t\t\tname = \"{}\"".format(name))

                    i += 1

            sb.we()
            sb.wl("\t\tif name != None:")
            sb.wl("\t\t\tmsg = \"Struct {} field {{}} is None\".format(name)".format(dtype_name))
            sb.we()
            sb.wl("\t\t\tif is_read:")
            sb.wl("\t\t\t\traise myrpc.Common.MessageBodyException(msg)")
            sb.wl("\t\t\telse:")
            sb.wl("\t\t\t\traise myrpc.Common.MessageEncodeException(msg)")
            sb.we()

        return sb.get_string()

    def _dtype_kind_struct_read(self, dtype, v):
        sb = StringBuilder()
        dtype_name = dtype.get_name()
        classn = self._get_dtype_classn(dtype_name)

        sb.wl("{} = {}()".format(v, classn))
        sb.wl("{}.{}(codec)".format(v, _STRUCT_READ))

        return sb.get_string()

    def _dtype_kind_struct_write(self, dtype, v):
        sb = StringBuilder()

        sb.wl("{}.{}(codec)".format(v, _STRUCT_WRITE))

        return sb.get_string()

    def _get_dtype_classn(self, name, prefix = ""):
        classn = "{}{}".format(prefix, name)

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

    def _get_args_seri_classn(self, name, prefix = ""):
        classn = "{}{}_{}".format(prefix, self._args_seri_classp, name)

        return classn

    def _get_result_seri_classn(self, name, prefix = ""):
        classn = "{}{}_{}".format(prefix, self._result_seri_classp, name)

        return classn

    def _get_codec_dtype_classn(self, dtype):
        codec_dtype = self._gtm.get_codec_dtype(dtype)
        if codec_dtype == None:
            raise InternalException("codec_dtype is None")

        classn = "{}.{}".format(self._codec_dtype_classp, codec_dtype)

        return classn

GeneratorBase.register_gen("py", PyGenerator)
