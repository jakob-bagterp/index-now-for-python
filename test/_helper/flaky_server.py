import threading
from collections.abc import Generator
from contextlib import contextmanager
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class FlakyEndpointServer(ThreadingHTTPServer):
    """Local IndexNow endpoint that fails the first requests before it succeeds. Each failure is either a dropped connection (like `RemoteDisconnected` from Yandex) or a status code."""

    def __init__(self, failures: list[HTTPStatus | None]) -> None:
        super().__init__(("127.0.0.1", 0), FlakyEndpointHandler)
        self.failures = failures
        self.request_count = 0

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}/indexnow"


class FlakyEndpointHandler(BaseHTTPRequestHandler):
    server: FlakyEndpointServer

    def _handle(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(content_length)
        self.server.request_count += 1
        if self.server.failures:
            failure = self.server.failures.pop(0)
            if failure is None:
                self.close_connection = True  # Close the connection without sending a response.
                return
            self._respond(failure)
            return
        self._respond(HTTPStatus.OK)

    def _respond(self, status: HTTPStatus) -> None:
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_GET = _handle
    do_POST = _handle

    def log_message(self, format: str, *args: object) -> None:
        pass


@contextmanager
def run_flaky_server(failures: list[HTTPStatus | None]) -> Generator[FlakyEndpointServer]:
    server = FlakyEndpointServer(list(failures))
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
