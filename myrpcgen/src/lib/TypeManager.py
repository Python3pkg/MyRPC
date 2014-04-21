from abc import ABCMeta, abstractmethod

from myrpcgen.Constants import RESULT_FIELD_NAME
from myrpcgen.ParserInternalException import ParserInternalException
from myrpcgen.InternalException import InternalException

_FID_STOP = 0xffff

class DataTypeKind:
    """Data type kind enum."""

    (# Primitive types:
     BINARY,
     STRING,
     BOOL,
     UI8,
     UI16,
     UI32,
     UI64,
     I8,
     I16,
     I32,
     I64,
     FLOAT,
     DOUBLE,
     # Enumerated type:
     ENUM,
     # Container types:
     LIST,
     STRUCT,
     EXC) = range(17)

class TypeBase(metaclass = ABCMeta):
    """Base class of all data types."""

    @abstractmethod
    def __init__(self, name, dtype_kind):
        self._name = name
        self._dtype_kind = dtype_kind
        self._container_compat = True

    def get_name(self):
        return self._name

    def get_dtype_kind(self):
        return self._dtype_kind

    def check_container_compat(self):
        if not self._container_compat:
            raise ParserInternalException("Type {} can't be used in containers".format(self._name))

class PrimitiveType(TypeBase):
    """Class for all builtin primitive types."""

    def __init__(self, name, dtype_kind):
        super().__init__(name, dtype_kind)

class EnumType(TypeBase):
    """Class for enumerated types."""

    def __init__(self, name):
        super().__init__(name, DataTypeKind.ENUM)

        self._entries = {}

    def get_entries(self):
        l = []

        for entry in self._entries.items():
            l.append(entry)

        l_sorted = sorted(l, key = lambda entry: entry[1])

        return l_sorted

    def get_values(self):
        values = set(self._entries.values())
        values_sorted = [str(value) for value in sorted(values)]

        return values_sorted

    def add_entry(self, name, value):
        if name in self._entries:
            raise ParserInternalException("{} is already specified in enum".format(name))

        self._entries[name] = value

class ListType(TypeBase):
    """Class for list types."""

    def __init__(self, name):
        super().__init__(name, DataTypeKind.LIST)

        self._elem_dtype = None

    def get_elem_dtype(self):
        return self._elem_dtype

    def set_elem_dtype(self, elem_dtype):
        elem_dtype.check_container_compat()

        self._elem_dtype = elem_dtype

class StructType(TypeBase):
    """Class for structure types."""

    def __init__(self, name):
        super().__init__(name, DataTypeKind.STRUCT)

        self._fieldh = FieldHandler()

    def get_fields(self):
        return self._fieldh.get_fields()

    def add_field(self, field):
        self._fieldh.add_field(field)

class ExcType(TypeBase):
    """Class for exception types."""

    def __init__(self, name):
        super().__init__(name, DataTypeKind.EXC)

        self._fieldh = FieldHandler()
        self._container_compat = False

    def get_fields(self):
        return self._fieldh.get_fields()

    def add_field(self, field):
        self._fieldh.add_field(field)

class Method:
    """Represent a method (methods live outside TypeManager namespace)."""

    def __init__(self, name):
        self._name = name
        # In and out structs are not registered with TypeManager.
        self._in_struct = StructType("args")
        self._out_struct = StructType("result")
        self._out_req = None
        self._out_dtype = None
        self._excs = {}

    def get_name(self):
        return self._name

    def get_in_struct(self):
        return self._in_struct

    def get_out_struct(self):
        return self._out_struct

    def get_excs(self):
        return self._excs.values()

    def has_result(self):
        r = (self._out_req != None)

        return r

    def add_in_field(self, field):
        self._in_struct.add_field(field)

    def set_out(self, req, dtype):
        if self._out_req != None:
            raise ParserInternalException("Method return value is already specified")

        self._out_req = req
        self._out_dtype = dtype

    def add_exc(self, exc):
        name = exc.get_name()
        if exc.get_dtype_kind() != DataTypeKind.EXC:
            raise ParserInternalException("Type {} is not an exception".format(name))
        if name in self._excs:
            raise ParserInternalException("Exception {} is already listed".format(name))

        self._excs[name] = exc

    def finalize(self):
        # Return value is handled by creating a struct with one element.

        if self._out_req != None:
            field = Field(0, self._out_req, self._out_dtype, RESULT_FIELD_NAME)
            self._out_struct.add_field(field)

class Field:
    """Represent a field."""

    def __init__(self, fid, req, dtype, name):
        self._fid = fid
        self._req = req
        self._dtype = dtype
        self._name = name

    def get_fid(self):
        return self._fid

    def get_req(self):
        return self._req

    def get_dtype(self):
        return self._dtype

    def get_name(self):
        return self._name

class FieldHandler:
    """Handler for fields."""

    def __init__(self):
        # Maintain field ordering, because of method args.
        self._fields = []
        self._fids = {}
        self._names = {}

    def add_field(self, field):
        fid = field.get_fid()
        if fid == _FID_STOP:
            raise ParserInternalException("Fid {} is reserved".format(fid))
        if fid in self._fids:
            raise ParserInternalException("Fid {} is already defined".format(fid))

        dtype = field.get_dtype()
        dtype.check_container_compat()

        name = field.get_name()
        if name in self._names:
            raise ParserInternalException("Field {} is already defined".format(name))

        self._fields.append(field)
        self._fids[fid] = field
        self._names[name] = field

    def get_fields(self):
        return self._fields

class TypeManager:
    """Type manager."""

    def __init__(self):
        self._dtypes = {}

        self._register_primitive_dtypes()

    def register_dtype(self, dtype):
        name = dtype.get_name()
        if name in self._dtypes:
            raise InternalException("dtype {} is already registered".format(name))

        self._dtypes[name] = dtype

    def lookup_dtype(self, name):
        """Lookup the specified data type.

        If data type is not exist, KeyError is thrown.
        """

        dtype = self._dtypes[name]

        return dtype

    def has_dtype(self, name):
        r = (name in self._dtypes)

        return r

    def list_dtype(self):
        dtypes = self._dtypes.values()

        return dtypes

    def _register_primitive_dtypes(self):
        self.register_dtype(PrimitiveType("binary", DataTypeKind.BINARY))
        self.register_dtype(PrimitiveType("string", DataTypeKind.STRING))
        self.register_dtype(PrimitiveType("bool",   DataTypeKind.BOOL))
        self.register_dtype(PrimitiveType("ui8",    DataTypeKind.UI8))
        self.register_dtype(PrimitiveType("ui16",   DataTypeKind.UI16))
        self.register_dtype(PrimitiveType("ui32",   DataTypeKind.UI32))
        self.register_dtype(PrimitiveType("ui64",   DataTypeKind.UI64))
        self.register_dtype(PrimitiveType("i8",     DataTypeKind.I8))
        self.register_dtype(PrimitiveType("i16",    DataTypeKind.I16))
        self.register_dtype(PrimitiveType("i32",    DataTypeKind.I32))
        self.register_dtype(PrimitiveType("i64",    DataTypeKind.I64))
        self.register_dtype(PrimitiveType("float",  DataTypeKind.FLOAT))
        self.register_dtype(PrimitiveType("double", DataTypeKind.DOUBLE))
