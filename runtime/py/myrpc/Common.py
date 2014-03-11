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

class MessageEncodeException(MyRPCException):
    """Serialize exception class."""

    def __init__(self, msg):
        super().__init__(msg)

class MessageDecodeException(MyRPCException):
    """Base class for deserialize-related exceptions."""

    def __init__(self, msg):
        super().__init__(msg)

class MessageTruncatedException(MessageDecodeException):
    """Thrown by transport implementation if the received message is truncated."""

    def __init__(self):
        super().__init__("Message is truncated")

class MessageHeaderException(MessageDecodeException):
    """Thrown by codec if there is a problem with the header of received message."""

    def __init__(self, msg):
        super().__init__(msg)

class MessageBodyException(MessageDecodeException):
    """Thrown by codec or deserializer if there is a problem."""

    def __init__(self, msg):
        super().__init__(msg)

class ServerErrorException(MyRPCException):
    """Thrown by client code if ERROR message is received from server."""

    def __init__(self, msg):
        super().__init__(msg)
