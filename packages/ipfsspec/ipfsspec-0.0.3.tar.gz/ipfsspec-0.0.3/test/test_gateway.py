import datetime
import json
from mockserver import mock_servers

import ipfsspec  # noqa: F401
import fsspec

from http.server import BaseHTTPRequestHandler
import urllib.parse


class BaseIPFSHandler(BaseHTTPRequestHandler):
    objects = {}

    def abort_before_request(self):
        return False

    def object_size(self, oid):
        return len(self.objects[oid].encode("utf-8"))

    def do_GET(self):
        if self.abort_before_request():
            return
        if self.path == "/api/v0/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"version": "0.1_test"}, ensure_ascii=False).encode("utf-8"))
        elif self.path.startswith("/ipfs/"):
            oid = self.path[6:]
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(self.object_size(oid)))
            self.end_headers()
            self.wfile.write(self.objects[oid].encode("utf-8"))

    def do_POST(self):
        if self.abort_before_request():
            return
        urlparts = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(urlparts.query)
        if urlparts.path == "/api/v0/object/stat":
            oid = query.get("arg", [])[0]
            res = {"Hash": oid, "NumLinks": 0, "DataSize": self.object_size(oid)}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))


def make_rate_limited_handler(max_rate, objects):
    request_count = [0]
    next_allowed_request = [datetime.datetime.now()]

    _objects = objects

    class RateLimitedHandler(BaseIPFSHandler):
        objects = _objects

        @classmethod
        def get_request_count(cls):
            return request_count[0]

        def apply_rate_limit(self):
            request_count[0] += 1
            now = datetime.datetime.now()
            if now <= next_allowed_request[0]:
                self.send_response(429)
                self.end_headers()
                return True
            else:
                next_allowed_request[0] = now + max_rate
                return False

        def abort_before_request(self):
            return self.apply_rate_limit()

    return RateLimitedHandler


def make_normal_handler(objects):
    _objects = objects

    class NormalHandler(BaseIPFSHandler):
        objects = _objects

    return NormalHandler


def make_incomplete_handler(objects):
    _objects = {k: o[:-1] for k, o in objects.items()}

    class IncompleteHandler(BaseIPFSHandler):
        objects = _objects

        def object_size(self, oid):
            return super().object_size(oid) + 1

    return IncompleteHandler


def test_backoff():
    handlers = [
        make_rate_limited_handler(
            datetime.timedelta(seconds=0.01),
            {"foo": "bar"}),
    ]
    with mock_servers(handlers) as gateways:
        fs = fsspec.filesystem("ipfs", gateways=gateways, timeout=1)
        for _ in range(100):
            with fs.open("foo") as f:
                assert f.read().decode("utf-8") == "bar"
        assert handlers[0].get_request_count() < 240


def test_backoff_use_faster_server():
    handlers = [
        make_rate_limited_handler(
            datetime.timedelta(seconds=0.1),
            {"foo": "zapp"}),
        make_rate_limited_handler(
            datetime.timedelta(seconds=0.01),
            {"foo": "zapp"}),
    ]
    with mock_servers(handlers) as gateways:
        fs = fsspec.filesystem("ipfs", gateways=gateways, timeout=1)
        for _ in range(100):
            with fs.open("foo") as f:
                assert f.read().decode("utf-8") == "zapp"
        assert handlers[0].get_request_count() < handlers[1].get_request_count()


def test_fallback_if_incomplete():
    handlers = [
        make_incomplete_handler(
            {"foo": "baz"}),
        make_normal_handler(
            {"foo": "baz"}),
    ]
    with mock_servers(handlers) as gateways:
        fs = fsspec.filesystem("ipfs", gateways=gateways, timeout=1)
        with fs.open("foo") as f:
            assert f.read().decode("utf-8") == "baz"
