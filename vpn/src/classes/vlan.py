class Vlan():
    """
    Class for vlans
    """
    def __init__(self, id, network, mask, hostNumber):
        self.id = id
        self.network = network
        self.mask = mask
        self.hostNumber = hostNumber