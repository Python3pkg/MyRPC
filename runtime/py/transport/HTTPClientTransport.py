import http.client
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

    def set_opener(self, opener):
        self._opener = opener

    def set_timeout(self, timeout):
        self._timeout = timeout

    def _reset(self):
        self._rf = None
        self._wf = io.BytesIO()

    def _flush(self):
        wbuf = self._wf.getvalue()

        req = urllib.request.Request(self._url, data = wbuf, method = "POST")
        req.add_header("Content-Type", "application/octet-stream")

        opener = self._opener.open if self._opener else urllib.request.urlopen

        try:
            resp = opener(req, timeout = self._timeout)
            rbuf = resp.read()
        except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
            # FIXME: Is it good idea to convert all of those exceptions to
            # HTTPClientException?

            raise HTTPClientException(e)

        self._rf = io.BytesIO(rbuf)

class HTTPClientException(TransportException):
    """Exception class for HTTP-related errors."""

    def __init__(self, reason):
        super().__init__(str(reason))

        self._reason = reason

    def get_reason(self):
        return self._reason
