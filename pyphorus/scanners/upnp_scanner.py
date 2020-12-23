import asyncio
from typing import List
from urllib.parse import urlparse

import aiohttp
import ssdpy
from defusedxml.ElementTree import fromstring

from pyphorus.devices import Device


class UPnP:

    def __init__(self, search_term: str = None, port: int = 1900):
        if search_term is None:
            search_term = "ssdp:all"
            
        self._ssdp_client = ssdpy.SSDPClient(port=port)
        self._search_term = search_term

    def scan(self) -> List[Device]:
        responses = self._ssdp_client.m_search(self._search_term)

        devices = []

        async def _scan():
            tasks = []
            async with aiohttp.ClientSession() as session:
                for resp in responses:
                    url = resp.get('location')
                    if ".xml" in url:
                        tasks.append(self._network_request(session, url))
                xmls = await asyncio.gather(*tasks)

                for x in xmls:
                    device = Device()

                    et = fromstring(x.strip())

                    for child in et:
                        if "URLBase" in child.tag:
                            url_base = child.text
                            if url_base is not None:

                                parsed_url = urlparse(url_base)
                                if ":" in parsed_url.netloc:
                                    device.ip, device.port = parsed_url.netloc.split(":")
                                else:
                                    device.ip = parsed_url.netloc

                        if "device" in child.tag:
                            for dev in child:
                                if "deviceType" in dev.tag:
                                    device.device_type = dev.text

                                if "friendlyName" in dev.tag:
                                    device.friendly_name = dev.text

                    if device.ip is not "":
                        device.is_open = True
                        devices.append(device)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(_scan())
        return devices

    async def _network_request(self, session, url):
        async with session.get(url) as response:
            return await response.text()
