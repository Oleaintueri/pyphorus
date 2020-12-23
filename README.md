<h1 align="center">Pyphorus</h1>

<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/Oleaintueri/pyphorus?style=flat-square">
    <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/v/tag/Oleaintueri/pyphorus?style=flat-square">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/pyphorus?style=flat-square">
</p>

---

A small network library written in Python 3.

Features:
 - Port scanner
 - UPnP client (SSDP wrapper)

Build with :heart: by 

<a href="https://oleaintueri.com"><img src="https://oleaintueri.com/images/oliv.svg" width="60px"/><img width="200px" style="padding-bottom: 10px" src="https://oleaintueri.com/images/oleaintueri.svg"/></a>

[Oleaintueri](https://oleaintueri.com) is sponsoring the development and maintenance of this project within their organisation.


## Getting started

### Installation

    pip install pyphorus
    
Or
    
    pip install git+https://github.com/Oleaintueri/pyphorus.git

### Usage

```python
import pyphorus

if __name__ == "__main__":
    phorus = pyphorus.Pyphorus()
    devices = phorus.scan_ports("192.168.0.1", ports=[80, 443, 9000], only_open=True)
    
    for device in devices:
        print(device.ip, device.port)
    
    devices = phorus.scan_upnp("ssdp:all")
    
    for device in devices:
        print(device.ip, device.friendly_name, device.device_type)
    
    # if you want only the unique ips to remain and are not interested in the ports
    unique_devices = pyphorus.utils.strip_duplicate_ips(devices)
    
    
```

### Testing

Pyphorus uses `nose` to run its tests and mock testing server.

    nosetests -v
    