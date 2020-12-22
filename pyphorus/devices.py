class Device(object):

    def __init__(self, ip: str, port: int, name: str = "", device_type: str = ""):
        self._ip = ip
        self._port = port
        self._name = name
        self._device_type = device_type
        self._is_open = False

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def is_open(self):
        return self._is_open

    @property
    def name(self):
        return self._name

    @property
    def device_type(self):
        return self._device_type

    @is_open.setter
    def is_open(self, is_open: bool):
        self._is_open = is_open

    @name.setter
    def name(self, name: str):
        self._name = name

    @device_type.setter
    def device_type(self, device_type: str):
        self._device_type = device_type
