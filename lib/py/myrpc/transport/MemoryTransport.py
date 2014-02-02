import io

from myrpc.Common import MessageTruncatedException
from myrpc.transport.TransportBase import TransportState, TransportBase

class MemoryTransport(TransportBase):
    """Provide memory-buffered transport."""

    def __init__(self, buf = None):
        """Initialize transport.

        If rbuf is specified, then its content is copied to the read memory buffer.
        """

        super().__init__()

        self._rf = io.BytesIO(buf)
        self._wf = io.BytesIO()

    def set_state(self, state):
        if state == TransportState.READ_END:
            self._rf.truncate(0)
        elif state == TransportState.WRITE_BEGIN:
            self._wf.truncate(0)

    def read(self, count):
        buf = self._rf.read(count)
        if len(buf) < count:
            raise MessageTruncatedException()

        return buf

    def write(self, buf):
        self._wf.write(buf)

    def get_value(self):
        """Return bytes containing the entire contents of the write memory buffer."""

        buf = self._wf.getvalue()

        return buf
