"""

 PACKNET  -  c0mplh4cks

 RAW



"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === Raw Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.protocol = None
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = len(self.data)

        packet.insert(0, self.data)     # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.data = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i
