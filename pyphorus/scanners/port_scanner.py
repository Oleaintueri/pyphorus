import asyncio
import ipaddress
from typing import List

import requests_threads

from pyphorus import Device


class PortScanner:

    def __init__(self, ip: str, ports: List[int] = None, timeout=2000, return_only_open=False):
        """
        Scan a the network for any open ports
        :param ip: a singular ip address eg. "192.168.0.1" or a cidr "192.168.0.1/24"
        :param ports: a list of ports. defaults are 80 and 443
        """
        if ports is None:
            ports = [80, 443]

        self._devices = []
        self._timeout = timeout
        self._return_only_open = return_only_open

        if "/" in ip:
            try:
                ips = list(ipaddress.ip_network(ip).hosts())

                for i in ips:
                    for y in ports:
                        self._devices.append(Device(i, y))

            except ValueError:
                raise ValueError("given ip address is not valid.")

        else:
            try:
                ipAddr = ipaddress.ip_address(ip)

                for y in ports:
                    self._devices.append(Device(str(ipAddr), y))

            except ValueError:
                raise ValueError("given ip address is not valid.")

        self.session = requests_threads.AsyncSession(n=len(self._devices))

    async def _network_request(self, device) -> Device:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(device.ip, device.port),
                                                    timeout=(self._timeout / 1000))
            writer.close()
            await writer.wait_closed()
            device.is_open = True
        except:
            device.is_open = False

        return device

    def scan(self) -> List[Device]:
        tasks = []

        async def _scan():
            for device in self._devices:
                tasks.append(self._network_request(device))

            self._devices = await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(_scan())

        if self._return_only_open:
            return list(filter(lambda x: x.is_open is True, self._devices))

        return self._devices
