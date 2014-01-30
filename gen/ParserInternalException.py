class ParserInternalException(Exception):
    """Internal parser exception class.

    It is allowed to be thrown in case of parsing errors only.
    """

    def __init__(self, msg):
        super().__init__()

        self._msg = str(msg)

    def __str__(self):
        return self._msg
