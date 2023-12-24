class Vlan():
    """
    Class for vlans
    """
    def __init__(self, id, network, mask):
        self.id = id
        self.network = network
        self.mask = mask