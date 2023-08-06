"""

 PACKNET  -  c0mplh4cks

 TCP

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







# === TCP Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.seq = 0
        self.ack = 0
        self.hlength = 0
        self.flags = 0b000000000
        self.win = 65000
        self.urg = 0
        self.length = 0
        self.checksum = 0
        self.options = []
        self.protocol = [ self.src[1], self.dst[1] ]
        self.data = b""



    def build(self):
        packet = {}

        options = b""
        for option in self.options:
            option.build()
            options += option.packet
        while len(options) %4 != 0:
            options = b"\x01" + options

        self.length = 20 + len(options) + len(self.data)
        self.hlength = (20 + len(options)) // 4
        self.flags += self.hlength << 12

        packet[0] = pack( ">H", self.src[1] )   # Source PORT
        packet[1] = pack( ">H", self.dst[1] )   # Target PORT
        packet[2] = pack( ">L", self.seq )      # Sequence number
        packet[3] = pack( ">L", self.ack )      # Acknowledgement number
        packet[4] = pack( ">H", self.flags )    # Flags & Header length
        packet[5] = pack( ">H", self.win )      # Window size
        packet[7] = pack( ">H", self.urg )      # Urgent pointer
        packet[6] = checksum( [                 # Checksum
            *packet.values(),
            encode.ip( self.src[0] ),
            encode.ip( self.dst[0] ),
            pack( ">H", 6 ),
            pack( ">H", self.length ),
        ] )
        packet[8] = options                     # Options
        packet[9] = self.data                   # Data

        self.protocol = [ self.src[1], self.dst[1] ]

        self.packet = b"".join([ value for key, value in sorted(packet.items()) ])

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.src[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Source PORT
        i, self.dst[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Target PORT
        i, self.seq         = i+4, unpack( ">L", packet[i:i+4] )[0]     # Sequence number
        i, self.ack         = i+4, unpack( ">L", packet[i:i+4] )[0]     # Acknowledgement number
        i, self.flags       = i+2, unpack( ">H", packet[i:i+2] )[0]     # Flags & Header length
        i, self.win         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Window size
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.urg         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Urgent pointer

        self.hlength = self.flags >> 12
        self.flags -= self.hlength << 12
        self.hlength = self.hlength * 4

        while i < self.hlength:                                         # Option
            option = Option( packet[i:self.hlength]  )
            i += option.read()
            self.options.append(option)

        i, self.data = i+len( packet[i:] ), packet[i:]                   # Data

        self.protocol = [ self.src[1], self.dst[1] ]

        self.length = i

        return i







# === Option === #
class Option:
    def __init__(self, packet=b""):
        self.packet = packet

        self.kind = 0
        self.length = 0
        self.mss = 0
        self.timestamp = 0
        self.timereply = 0
        self.scale = 0
        self.leftedge = 0
        self.rightedge = 0
        self.data = b""



    def build(self):
        packet = {}

        packet[0] = pack( ">B", self.kind )

        if self.kind == 2:                          # Maximum segment size
            packet[2] = encode.tobyte( self.mss )
            self.length = len(b"".join(packet)) +1
            packet[1] = pack( ">B", self.length )

        elif self.kind == 3:                        # Window scale
            packet[2] = encode.tobyte( self.scale )
            self.length = len(b"".join(packet)) +1
            packet[1] = pack( ">B", self.length )

        elif self.kind == 4:                        # SACK (Selective ACKnowledgement) permitted
            self.length = 2
            packet[1] = pack( ">B", self.length )

        elif self.kind == 5:                        # SACK (Selective ACKnowledgement)
            self.length = 10
            packet[1] = pack( ">B", self.length )
            packet[2] = pack( ">L", self.leftedge )
            packet[3] = pack( ">L", self.rightedge )

        elif self.kind == 8:                        # Timestamps
            self.length = 10
            packet[1] = pack( ">B", self.length )
            packet[2] = pack( ">L", self.timestamp )
            packet[3] = pack( ">L", self.timereply )

        self.packet = b"".join([ value for key, value in sorted(packet.items()) ])

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.kind = i+1, unpack( ">B", packet[i:i+1] )[0]

        if self.kind == 2:                                              # Maximum segment size
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.mss = i+(self.length-2), decode.toint( packet[i:i+(self.length-2)] )

        elif self.kind == 3:                                            # Window scale
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.scale = i+(self.length-2), decode.toint( packet[i:i+(self.length-2)] )

        elif self.kind == 4:                                            # SACK (Selective ACKnowledgement) permitted
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.data = i+(self.length-2), packet[i:i+(self.length-2)]

        elif self.kind == 5:                                            # SACK (Selective ACKnowledgement)
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.leftedge = i+4, unpack( ">L", packet[i:i+4] )[0]
            i, self.rightedge = i+4, unpack( ">L", packet[i:i+4] )[0]

        elif self.kind == 8:                                            # Timestamps
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.timestamp = i+4, unpack( ">L", packet[i:i+4] )[0]
            i, self.timereply = i+4, unpack( ">L", packet[i:i+4] )[0]

        self.length = i

        return i
