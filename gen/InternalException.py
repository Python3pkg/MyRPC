class InternalException(Exception):
    """Exception class for all MyRPCgen internal errors.

    This exception should not be caught, since it represents an
    internal error in MyRPCgen logic.
    """

    def __init__(self, msg):
        super().__init__(msg)
