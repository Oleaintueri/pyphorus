from typing import List

from pyphorus.devices import Device
from pyphorus.scanners.port_scanner import PortScanner
from pyphorus.scanners.upnp_scanner import UPnP


class Pyphorus:

    def __init__(self, timeout: int = 2000):
        self._timeout = timeout

    def scan_ports(self, ip, ports: List[int]) -> List[Device]:
        port_scanner = PortScanner(ip, ports, return_only_open=True)
        return port_scanner.scan()

    def scan_upnp(self, search_term: str = "rootdevice") -> List[Device]:
        upnp = UPnP()
        return upnp.scan()
