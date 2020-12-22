import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests
from nose.tools import assert_equal

from pyphorus.pyphorus import Pyphorus


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(requests.codes.ok)
        self.end_headers()
        return


class TestPyphorus(object):

    @classmethod
    def setup_class(cls):
        # Configure mock server.
        cls.mock_server_port = 8000
        cls.mock_server = HTTPServer(('127.0.0.1', cls.mock_server_port), MockServerRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

    def test_port_scanner(self):
        phorus = Pyphorus()
        devices = phorus.scan_ports(ip="127.0.0.1", ports=[90, 1000, 8000, 80])

        device = list(filter(lambda x: x.is_open is True and x.port == 8000, devices))

        assert_equal(len(device), 1)

        assert_equal(device[0].port, 8000)
