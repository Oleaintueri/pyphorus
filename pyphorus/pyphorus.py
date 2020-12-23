from typing import List

from pyphorus import Device
from pyphorus.scanners import PortScanner
from pyphorus.scanners import UPnP


class Pyphorus:

    def __init__(self, timeout: int = 2000):
        self._timeout = timeout

    def scan_ports(self, ip, ports: List[int], only_open: bool = True) -> List[Device]:
        """
        Scan for open ports
        :param ip: a singular ip address or cidr
        :param ports: list of ports to scan
        :param only_open: only return the devices with open ports
        :return:
        """
        port_scanner = PortScanner(ip, ports, return_only_open=only_open)
        return port_scanner.scan()

    def scan_upnp(self, search_term: str = "upnp:rootdevice") -> List[Device]:
        upnp = UPnP(search_term)
        return upnp.scan()
