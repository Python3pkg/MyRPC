import re

from myrpcgen.Constants import RESERVED_PREFIXES, ENCODING, IDENTIFIER_RE
from myrpcgen.ParserInternalException import ParserInternalException
from myrpcgen.TypeManager import EnumType, ListType, StructType, ExcType, Method, Field, TypeManager
from myrpcgen.GeneratorBase import GeneratorBase

class ParserContext:
    """Parser context enum."""

    (MAIN,
     ENUM,
     STRUCT,
     EXC,
     METHOD) = range(5)

class Parser:
    """MyRPC IDL parser implementation."""

    def __init__(self, filename):
        self._filename = filename
        self._lineno = 0

        self._namespaces = {}
        self._tm = TypeManager()
        self._methods = {}

        self._curr_dtype = None
        self._curr_method = None

        self._next_enum_value = None

        self._setup_kws()
        self._set_context(ParserContext.MAIN)

    def parse(self):
        try:
            self._parse()
        except ParserInternalException as e:
            raise ParserException(e, self._lineno)

    def get_namespaces(self):
        return self._namespaces

    def get_tm(self):
        return self._tm

    def get_methods(self):
        return self._methods.values()

    def _parse(self):
        try:
            f = open(self._filename, mode = "rt", encoding = ENCODING)
            lines = f.readlines()
            f.close()
        except OSError as e:
            raise ParserInternalException(e)

        # Process IDL file.

        for line in lines:
            # Increase line number counter.

            self._lineno += 1

            # Remove comments and skip empty lines.

            i = line.find("#")
            if i >= 0:
                line = line[:i]

            line = line.strip()

            if len(line) == 0:
                continue

            # Lookup and execute keyword func.

            self._tok = Tokenizer(self._tm, line)

            kws = self._kws[self._get_context()]
            kw = self._tok.get_kw()

            try:
                func = kws[kw]
            except KeyError:
                raise ParserInternalException("Unknown keyword {}".format(kw))

            func()

            self._tok.eol()

        # At EOF, context has to be MAIN.

        if self._get_context() != ParserContext.MAIN:
            raise ParserInternalException("Unterminated context")

    # MAIN context

    def _main_namespace(self):
        gen_name = self._tok.get_gen_name()
        namespace = self._tok.get_ns()

        if gen_name in self._namespaces:
            raise ParserInternalException("Namespace for {} is already defined".format(gen_name))

        self._namespaces[gen_name] = namespace

    def _main_list(self):
        name = self._tok.get_id()
        self._check_dtype_name(name)

        elem_dtype = self._tok.get_dtype()

        dtype = ListType(name)
        dtype.set_elem_dtype(elem_dtype)

        self._tm.register_dtype(dtype)

    def _main_beginenum(self):
        name = self._tok.get_id()
        self._check_dtype_name(name)

        self._curr_dtype = EnumType(name)
        self._next_enum_value = 0

        self._set_context(ParserContext.ENUM)

    def _main_beginstruct(self):
        name = self._tok.get_id()
        self._check_dtype_name(name)

        self._curr_dtype = StructType(name)

        self._set_context(ParserContext.STRUCT)

    def _main_beginexception(self):
        name = self._tok.get_id()
        self._check_dtype_name(name)

        self._curr_dtype = ExcType(name)

        self._set_context(ParserContext.EXC)

    def _main_beginmethod(self):
        name = self._tok.get_id()
        if name in self._methods:
            raise ParserInternalException("Method {} is already defined".format(name))

        self._curr_method = Method(name)
        self._methods[name] = self._curr_method

        self._set_context(ParserContext.METHOD)

    # ENUM context

    def _enum_entry(self):
        name = self._tok.get_id()

        value = self._tok.get_i32(req = False)
        if value == None:
            value = self._next_enum_value

        self._next_enum_value = value + 1 # FIXME: overflow i32

        self._curr_dtype.add_entry(name, value)

    def _enum_endenum(self):
        self._tm.register_dtype(self._curr_dtype)

        self._curr_dtype = None
        self._next_enum_value = None

        self._set_context(ParserContext.MAIN)

    # STRUCT context

    def _struct_field(self):
        fid = self._tok.get_fid()
        req = self._tok.get_req()
        dtype = self._tok.get_dtype()
        name = self._tok.get_id()

        field = Field(fid, req, dtype, name)
        self._curr_dtype.add_field(field)

    def _struct_endstruct(self):
        self._tm.register_dtype(self._curr_dtype)

        self._curr_dtype = None

        self._set_context(ParserContext.MAIN)

    # EXC context

    def _exc_field(self):
        fid = self._tok.get_fid()
        req = self._tok.get_req()
        dtype = self._tok.get_dtype()
        name = self._tok.get_id()

        field = Field(fid, req, dtype, name)
        self._curr_dtype.add_field(field)

    def _exc_endexception(self):
        self._tm.register_dtype(self._curr_dtype)

        self._curr_dtype = None

        self._set_context(ParserContext.MAIN)

    # METHOD context

    def _method_in(self):
        fid = self._tok.get_fid()
        req = self._tok.get_req()
        dtype = self._tok.get_dtype()
        name = self._tok.get_id()

        field = Field(fid, req, dtype, name)
        self._curr_method.add_in_field(field)

    def _method_out(self):
        req = self._tok.get_req()
        dtype = self._tok.get_dtype()

        self._curr_method.set_out(req, dtype)

    def _method_throw(self):
        exc = self._tok.get_dtype()

        self._curr_method.add_exc(exc)

    def _method_endmethod(self):
        self._curr_method.finalize()
        self._curr_method = None

        self._set_context(ParserContext.MAIN)

    # ---

    def _setup_kws(self):
        self._kws = {
            ParserContext.MAIN: {
                "namespace":      self._main_namespace,
                "list":           self._main_list,
                "beginenum":      self._main_beginenum,
                "beginstruct":    self._main_beginstruct,
                "beginexception": self._main_beginexception,
                "beginmethod":    self._main_beginmethod
            },
            ParserContext.ENUM: {
                "entry":   self._enum_entry,
                "endenum": self._enum_endenum
            },
            ParserContext.STRUCT: {
                "field":     self._struct_field,
                "endstruct": self._struct_endstruct
            },
            ParserContext.EXC: {
                "field":        self._exc_field,
                "endexception": self._exc_endexception
            },
            ParserContext.METHOD: {
                "in":        self._method_in,
                "out":       self._method_out,
                "throw":     self._method_throw,
                "endmethod": self._method_endmethod
            }
        }

    def _get_context(self):
        return self._context

    def _set_context(self, context):
        self._context = context

    def _check_dtype_name(self, name):
        if self._tm.has_dtype(name):
            raise ParserInternalException("Type {} is already defined".format(name))

class Tokenizer:
    """Tokenizer implementation."""

    def __init__(self, tm, line):
        self._tm = tm
        self._toks = line.split()
        self._pos = 0

    def get_kw(self):
        tok = self._get_tok()

        return tok

    def get_id(self):
        tok = self._get_tok()

        if not re.match(IDENTIFIER_RE, tok):
            raise ParserInternalException("Valid identifier name expected")
        if tok.startswith(RESERVED_PREFIXES):
            raise ParserInternalException("Identifier begins with reserved string ({})".format(", ".join(RESERVED_PREFIXES)))

        return tok

    def get_fid(self):
        fid_min = 0
        fid_max = 0xffff

        try:
            fid = self._get_int(fid_min, fid_max)
        except ValueError:
            raise ParserInternalException("Field identifier must be numeric ({} ... {})".format(fid_min, fid_max))

        return fid

    def get_req(self):
        tok = self._get_tok()

        if tok == "required":
            r = True
        elif tok == "optional":
            r = False
        else:
            raise ParserInternalException("required/optional expected")

        return r

    def get_dtype(self):
        tok = self._get_tok()

        try:
            dtype = self._tm.lookup_dtype(tok)
        except KeyError:
            raise ParserInternalException("Type {} doesn't exist".format(tok))

        return dtype

    def get_gen_name(self):
        tok = self._get_tok()

        try:
            GeneratorBase.lookup_gen(tok)
        except KeyError:
            raise ParserInternalException("Generator {} is unknown".format(tok))

        return tok

    def get_ns(self):
        tok = self._get_tok()

        # Namespace check will take place later, during generator initialization.

        return tok

    def get_i32(self, req = True):
        int_min = -2147483648
        int_max = 2147483647

        try:
            i = self._get_int(int_min, int_max, req = req)
        except ValueError:
            raise ParserInternalException("Integer expected ({} ... {})".format(int_min, int_max))

        return i

    def eol(self):
        if self._pos < len(self._toks):
            raise ParserInternalException("End of line expected")

    def _get_int(self, min_value, max_value, req = True):
        """Parse integer.

        On failure, ValueError is thrown.
        """

        tok = self._get_tok(req = req)
        if tok == None:
            return None

        i = int(tok)
        if (i < min_value or i > max_value):
            raise ValueError()

        return i

    def _get_tok(self, req = True):
        if self._pos == len(self._toks):
            if req:
                raise ParserInternalException("Token expected")
            else:
                return None

        tok = self._toks[self._pos]
        self._pos += 1

        return tok

class ParserException(Exception):
    """Parser exception class."""

    def __init__(self, msg, lineno):
        super().__init__()

        self._msg = str(msg)
        self._lineno = lineno

    def __str__(self):
        s = ""

        if self._lineno > 0:
            s += "At line number {}: ".format(self._lineno)

        s += self._msg

        return s
