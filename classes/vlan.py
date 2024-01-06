import ipaddress


class Vlan():
    """
    Class for vlans
    """
    def __init__(self, id, network, mask):
        self.id = id
        self.network = network
        self.mask = mask
        self.hostNumber = self.__get_max_hosts()


    def __get_max_hosts(self):
        "Calculates the maximum number of hosts that a vlan supports"
        # Create a network object using address and mask
        network = ipaddress.IPv4Network(self.network + '/' + self.mask, strict=False)

        # Calculate the maximum number of computers in the VLAN
        max_hosts = network.num_addresses - 2  # Subtract network and broadcast address

        return max_hosts
    
    def get_all_ips(self):
        networkc = ipaddress.IPv4Network(self.network + '/' + self.mask, strict=False)
        ips = networkc.hosts()
        return ips