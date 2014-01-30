class MyRPCException(Exception):
    """Base class for all MyRPC exceptions."""

    def __init__(self, msg):
        super().__init__(msg)

        self._msg = msg

    def get_msg(self):
        return self._msg

class MyRPCInternalException(Exception):
    """Exception class for all MyRPC internal errors.

    This exception should not be caught, since it represents an
    internal error in MyRPC logic.
    """

    def __init__(self, msg):
        super().__init__(msg)

        self._msg = msg

    def get_msg(self):
        return self._msg

class MessageTypeException(MyRPCException):
    """Message type exception class."""

    def __init__(self, msg):
        super().__init__(msg)

class SerializerException(MyRPCException):
    """Serializer exception class."""

    def __init__(self, msg):
        super().__init__(msg)

class DeserializerException(MyRPCException):
    """Deserializer exception class."""

    def __init__(self, msg):
        super().__init__(msg)
