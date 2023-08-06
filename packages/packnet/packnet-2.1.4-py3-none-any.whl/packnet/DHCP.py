"""

 PACKNET  -  c0mplh4cks

 ETHERNET

     #===#==============#
     # 7 # Application  #
     #===#==============#
     | 6 | Presentation |
     |---|--------------|
     | 5 | Session      |
     |---|--------------|
     | 4 | Transport    |
     |---|--------------|
     | 3 | Network      |
     |---|--------------|
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === DHCP Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.op = 1
        self.ht = 1
        self.hl = 6
        self.hops = 0
        self.id = 0
        self.secelapsed = 0
        self.flags = 0b0000
        self.clientipaddr = ""
        self.youripaddr = ""
        self.serveripaddr = ""
        self.gatewayipaddr = ""
        self.clienthwaddr = ""
        self.padding = b""
        self.magiccookie = 0x63825363
        self.options = []
        self.protocol = None
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        clienthwaddr = encode.mac( self.clienthwaddr )
        clienthwaddr += ( 16 - self.hl ) * b"\x00"
        self.padding = 192 * b"\x00"

        packet.insert(0, pack( ">B", self.op ))             # Operation code
        packet.insert(1, pack( ">B", self.ht ))             # Hardware type
        packet.insert(2, pack( ">B", self.hl ))             # Hardware length
        packet.insert(3, pack( ">B", self.hops ))           # Hops
        packet.insert(4, pack( ">L", self.id ))             # Transaction identifier
        packet.insert(5, pack( ">H", self.secelapsed ))     # Seconds elapsed
        packet.insert(6, pack( ">H", self.flags ))          # Flags
        packet.insert(7, encode.ip( self.clientipaddr ))    # Client IP address
        packet.insert(8, encode.ip( self.youripaddr ))      # Your IP address
        packet.insert(9, encode.ip( self.serveripaddr ))    # Server IP address
        packet.insert(10, encode.ip( self.gatewayipaddr ))  # Gateway IP address
        packet.insert(11, clienthwaddr )                    # Client hardware address
        packet.insert(12, self.padding )                    # Padding
        packet.insert(13, pack( ">L", self.magiccookie ))   # Magic cookie

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.op              = i+1, packet[i]                            # Operation code
        i, self.ht              = i+1, packet[i]                            # Hardware type
        i, self.hl              = i+1, packet[i]                            # Hardware length
        i, self.hops            = i+1, packet[i]                            # Hops
        i, self.id              = i+4, unpack( ">L", packet[i:i+4] )[0]     # Transaction identifier
        i, self.secelapsed      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Seconds elapsed
        i, self.flags           = i+2, unpack( ">H", packet[i:i+2] )[0]     # Flags
        i, self.clientipaddr    = i+4, decode.ip( packet[i:i+4] )           # Client IP address
        i, self.youripaddr      = i+4, decode.ip( packet[i:i+4] )           # Your IP address
        i, self.serveripaddr    = i+4, decode.ip( packet[i:i+4] )           # Server IP address
        i, self.gatewayipaddr   = i+4, decode.ip( packet[i:i+4] )           # Gateway IP address
        i, clienthwaddr         = i+16, packet[i:i+16]                      # Client hardware address
        i, padding              = i+192, packet[i:i+192]                    # Padding
        i, self.magiccookie     = i+4, unpack( ">H", packet[i:i+4] )[0]     # Magic cookie

        if self.ht == 1 and self.hl == 6:
            self.clienthwaddr = decode.mac( clienthwaddr[:6] )

        self.length = i

        return i







# === Option === #
class Option:
    def __init__(self, packet=b""):
        self.packet = packet

        self.code = 0
        self.length = 0
        self.blen = 0
        #
        self.subnetmask = ""
        self.timeoffset = 0
        self.ipaddrs = []
        self.hostname = ""
        self.filesize = 0
        self.meritdumpfile = ""
        #
        self.data = b""



    def build(self):
        packet = []

        packet.insert(0, pack( ">B", self.code ))           # Code

        if self.code == 1:                                  # Subnetmask
            self.data += encode.ip( self.subnetmask )

        elif self.code == 2:                                # Time offset (?)
            self.data += pack( ">L", self.timeoffset )

        elif (3 <= self.code <= 11):                        # Router + Server options
            self.data += b"".join([ encode.ip( ip ) for ip in self.ipaddrs ])

        elif self.code == 12:                               # Hostname
            self.data += self.hostname.encode()

        elif self.code == 13:                               # File size
            self.data += pack( ">H", self.filesize )

        elif self.code == 14:                               # Merit dump file
            self.data += self.meritdumpfile.encode()

        elif self.code == 15:
            pass

        self.blen = len(self.data)                          # Length
        packet.insert(1, pack( ">B", blen ))
        packet.insert(2, self.data)

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.code = i+1, packet[i]                       # Code

        if self.code != 255 and self.code != 0:             # Length
            i, blen = i+1, packet[i]

        if self.code == 1:                                  # Subnetmask
            i, self.subnetmask = i+blen, decode.ip( packet[i:i+blen] )

        elif self.code == 2:                                # Time offset
            i, self.timeoffset = i+blen, packet[i:i+blen]

        elif (3 <= self.code <= 11):                        # Router + Server options
            #i, self.ipaddrs = i+blen, [ decode.ip(  )]
            for _ in range( blen//4 ):
                i, ip = i+4, decode.ip( packet[i:i+4] )
                self.ipaddrs.append( ip )

        elif self.code == 12:                               # Hostname
            i, self.hostname = i+blen, packet[i:i+blen].decode()

        elif self.code == 13:                               # File size
            i, self.filesize = i+2, unpack( ">H", packet[i:i+2] )

        elif self.code == 14:                               # Merit dump file
            i, self.meritdumpfile = i+blen, packet[i:i+blen].decode()


        self.blen = blen
        self.length = i

        return i
