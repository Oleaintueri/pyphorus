from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from xml.etree import ElementTree

import requests
import ssdpy
from nose.tools import assert_equal

import pyphorus


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '.xml' in self.path:
            base = ElementTree.Element('base')
            urlbase = ElementTree.SubElement(base, 'URLBase')
            urlbase.text = f'http://127.0.0.1:6735'
            device = ElementTree.SubElement(base, 'device')
            device_type = ElementTree.SubElement(device, 'deviceType')
            device_type.text = 'upnp:unique_pyphorus_id'
            device_friendly_name = ElementTree.SubElement(device, 'friendlyName')
            device_friendly_name.text = 'Pyphorus UPnP Server'

            out = ElementTree.tostring(base, encoding="unicode")
            self.send_response(requests.codes.ok)
            # Add response headers.
            self.send_header('Content-Type', 'application/xml; charset=utf-8')
            self.end_headers()

            # Add response content.
            self.wfile.write(out.encode('utf-8'))
        else:
            # Process an HTTP GET request and return a response with an HTTP 200 status.
            self.send_response(requests.codes.ok)
            self.end_headers()
        return


class TestPyphorus(object):

    @classmethod
    def setup_class(cls):
        # Configure mock servers.

        ports = [8000, 9000, 9001]

        for p in ports:
            cls.mock_server_port = p
            cls.mock_server = HTTPServer(('127.0.0.1', cls.mock_server_port), MockServerRequestHandler)

            # Start running mock server in a separate thread.
            # Daemon threads automatically shut down when the main process exits.
            cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
            cls.mock_server_thread.setDaemon(True)
            cls.mock_server_thread.start()

        # UPnP server
        cls.mock_upnp_server = HTTPServer(('127.0.0.1', 6735), MockServerRequestHandler)
        cls.mock_upnp_server_thread = Thread(target=cls.mock_upnp_server.serve_forever)
        cls.mock_upnp_server_thread.setDaemon(True)
        cls.mock_upnp_server_thread.start()

        cls.mock_ssdp_server = ssdpy.SSDPServer(usn="pyphorus_upnp_server", device_type="upnp:unique_pyphorus_id",
                                                location='http://127.0.0.1:6735/device.xml')
        cls.mock_ssdp_server_thread = Thread(target=cls.mock_ssdp_server.serve_forever)
        cls.mock_ssdp_server_thread.setDaemon(True)
        cls.mock_ssdp_server_thread.start()

    def test_port_scanner(self):
        phorus = pyphorus.Pyphorus()
        devices = phorus.scan_ports(ip="127.0.0.1", ports=[90, 1000, 8000, 9000, 9001])

        device = list(filter(lambda x: x.is_open is True and x.port == 8000, devices))

        assert_equal(len(device), 1)

        assert_equal(device[0].port, 8000)

    def test_upnp_scanner(self):
        phorus = pyphorus.Pyphorus()
        devices = phorus.scan_upnp("upnp:unique_pyphorus_id")

        assert_equal(len(devices), 1)
        assert_equal(devices[0].device_type, "upnp:unique_pyphorus_id")
