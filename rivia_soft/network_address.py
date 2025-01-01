from netifaces import AF_INET, AF_INET6, ifaddresses, interfaces
from socket import gethostname



class InterfaceAddresses:
    def __init__(self, interface:str, ipv4_addr:list[str]=[], ipv6_addr:list[str]=[]):
        self.interface: str = interface
        self.ipv4_addr: list[str] = ipv4_addr
        self.ipv6_addr: list[str] = ipv6_addr
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(if={self.interface}, v4={self.ipv4_addr}, v6={self.ipv6_addr})"

    def __repr__(self):
        return str(self)


def get_all_interface_addresses() -> list[InterfaceAddresses]:
    interfaces_ = interfaces()
    addresses: list[InterfaceAddresses] = []
    for interface in interfaces_:
        interface_addresses = ifaddresses(interface)
        ipv4_addr = [ addr['addr'] for addr in interface_addresses.get(AF_INET, []) ]
        ipv6_addr = [ addr['addr'] for addr in interface_addresses.get(AF_INET6, []) ]
        addresses.append(InterfaceAddresses(interface, ipv4_addr, ipv6_addr))
    return addresses

def get_all_ipv4_addresses() -> list[str]:
    ipv4_addresses = []
    for if_addr in get_all_interface_addresses():
        ipv4_addresses += if_addr.ipv4_addr
    return ipv4_addresses

def get_all_ipv6_addresses() -> list[str]:
    ipv6_addresses = []
    for if_addr in get_all_interface_addresses():
        ipv6_addresses += if_addr.ipv6_addr
    return ipv6_addresses

def get_hostname() -> str:
    return gethostname()

