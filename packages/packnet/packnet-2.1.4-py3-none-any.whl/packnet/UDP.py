"""

 PACKNET  -  c0mplh4cks

 UDP

     .---.--------------.
     | 7 | Application  |
     |---|--------------|
     | 6 | Presentation |
     |---|--------------|
     | 5 | Session      |
     #===#==============#
     # 4 # Transport    #
     #===#==============#
     | 3 | Network      |
     |---|--------------|
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === UDP Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.length = 0
        self.checksum = 0
        self.protocol = [ self.src[1], self.dst[1] ]
        self.data = b""



    def build(self):
        packet = {}

        self.length = 8 + len(self.data)

        packet[0] = pack( ">H", self.src[1] )   # Source PORT
        packet[1] = pack( ">H", self.dst[1] )   # Target PORT
        packet[2] = pack( ">H", self.length )   # Total length
        packet[4] = self.data                   # Data
        packet[4] = checksum( [                 # Checksum
            *packet.values(),
            encode.ip( self.src[0] ),
            encode.ip( self.dst[0] ),
            pack( ">H", 17 ),
            pack( ">H", self.length )
        ] )

        self.protocol = [ self.src[1], self.dst[1] ]

        self.packet = b"".join([ value for key, value in sorted(packet.items()) ])

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.src[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Source PORT
        i, self.dst[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Target PORT
        i, length           = i+2, unpack( ">H", packet[i:i+2] )[0]     # Total length
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.protocol = [ self.src[1], self.dst[1] ]

        self.length = i

        return i
