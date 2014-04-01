# FIXME: content-length

import io
import urllib.request
import urllib.error

from myrpc.Common import MessageTruncatedException
from myrpc.transport.TransportBase import TransportState, TransportBase, TransportException

class HTTPClientTransport(TransportBase):
    """Provide HTTP client transport."""

    def __init__(self, url):
        super().__init__()

        self._url = url
        self._timeout = None
        self._opener = None

    def set_state(self, state):
        if state == TransportState.WRITE_BEGIN:
            self._reset()
        elif state == TransportState.WRITE_END:
            self._flush()

    def read(self, count):
        buf = self._rf.read(count)
        if len(buf) < count:
            raise MessageTruncatedException()

        return buf

    def write(self, buf):
        self._wf.write(buf)

    def set_timeout(self, timeout):
        self._timeout = timeout

    def set_opener(self, opener):
        self._opener = opener

    def _reset(self):
        self._rf = None
        self._wf = io.BytesIO()

    def _flush(self):
        wbuf = self._wf.getvalue()

        req = urllib.request.Request(self._url, data = wbuf, method = "POST")
        req.add_header("Content-Type", "application/octet-stream")

        opener = self._opener if self._opener else urllib.request.build_opener() # FIXME

        try:
            resp = opener.open(req, timeout = self._timeout) # FIXME: timeout
        except urllib.error.URLError as e:
            raise TransportException(str(e)) # FIXME: exc

        rbuf = resp.read() # FIXME: exc
        self._rf = io.BytesIO(rbuf)
