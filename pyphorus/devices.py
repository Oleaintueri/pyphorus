class Device(object):

    def __init__(self, ip: str = "", port: int = 0, name: str = "", device_type: str = ""):
        self._ip = ip
        self._port = port
        self._name = name
        self._device_type = device_type
        self._friendly_name = ""
        self._is_open = False

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def friendly_name(self) -> str:
        return self._friendly_name

    @property
    def port(self) -> int:
        return self._port

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def name(self) -> str:
        return self._name

    @property
    def device_type(self) -> str:
        return self._device_type

    @ip.setter
    def ip(self, ip: str):
        self._ip = ip

    @port.setter
    def port(self, port: int):
        self._port = port

    @is_open.setter
    def is_open(self, is_open: bool):
        self._is_open = is_open

    @name.setter
    def name(self, name: str):
        self._name = name

    @device_type.setter
    def device_type(self, device_type: str):
        self._device_type = device_type

    @friendly_name.setter
    def friendly_name(self, friendly_name: str):
        self._friendly_name = friendly_name
