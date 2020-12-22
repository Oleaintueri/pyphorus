from pyphorus.pyphorus import Pyphorus

if __name__ == "__main__":
    phorus = Pyphorus()

    # devices = phorus.scan_upnp("ssdp:all")

    devices = phorus.scan_ports("192.168.43.0/24", ports=[80, 8000, 9000, 9001, 9090, 8080, 443, 22])
    for device in devices:
        print(device.name, device.ip, device.port)