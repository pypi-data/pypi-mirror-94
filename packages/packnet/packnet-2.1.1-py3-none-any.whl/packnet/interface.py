"""

 PACKNET  -  c0mplh4cks

 INTERFACE


"""





# === Importing Dependencies === #
import socket
from time import time
from .standards import encode, decode
from .packager import Packager
from . import ETHERNET
from . import ARP







# === Interface === #
class Interface():
    def __init__(self, card=None, port=0, passive=False):
        self.passive = passive
        self.timeout = 1

        self.sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003) )


        if not card:
            self.card = [ i[1] for i in socket.if_nameindex() ][-1]
        else:
            self.card = card

        if not passive:
            s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            s.setsockopt( socket.SOL_SOCKET, 25, f"{ self.card }".encode() )
            s.connect( ("1.1.1.1", 80) )
            ip = s.getsockname()[0]

            self.sock.bind( (self.card, 0) )
            mac = decode.mac( self.sock.getsockname()[4] )

            self.addr = ( ip, port, mac )



    def send(self, packet):
        self.sock.send(packet)

    def recv(self, length=2048):
        return self.sock.recvfrom(length)



    def getmac(self, ip):
        if self.passive: return None

        src = self.addr
        dst = [ip, 0, "ff:ff:ff:ff:ff:ff"]

        package = Packager()
        package.fill( ARP.Header, src, dst )
        package.layer[1].op = 1
        package.build()

        self.send( package.packet )


        start = time()
        while ( time()-start < self.timeout ):
            packet, info = self.recv()

            package = Packager(packet)
            package.read()

            if len( package.layer ) < 2: continue
            if type( package.layer[1] ) != ARP.Header: continue
            if package.layer[1].dst[2] != self.addr[2]: continue
            if package.layer[1].src[0] != ip: continue

            return package.layer[1].src
