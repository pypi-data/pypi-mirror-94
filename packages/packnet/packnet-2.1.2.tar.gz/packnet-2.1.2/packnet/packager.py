"""

 PACKNET  -  c0mplh4cks

 PACKAGER


"""





# === Importing Dependencies === #
from . import ETHERNET
from . import ARP, IPv4, ICMP
from . import UDP, TCP
from . import DNS, MQTT
from . import RAW







# === Packager === #
class Packager():
    def __init__(self, packet=b""):
        self.packet = packet

        self.layer = []

        self.tree = [
            [ ETHERNET.Header, IPv4.Header, 0x0800 ],
            [ ETHERNET.Header, ARP.Header, 0x0806 ],
            [ IPv4.Header, ICMP.Header, 1 ],
            [ IPv4.Header, UDP.Header, 17 ],
            [ IPv4.Header, TCP.Header, 6 ],
            [ UDP.Header, DNS.Header, 53 ],
            [ TCP.Header, MQTT.Header, 1883 ],
        ]



    def checkprotocol(self, protocol):
        if protocol.protocol == None: return RAW.Header

        l = protocol.protocol
        l = [l] if type(l) == int else l

        for p in list(l):
            for node in self.tree:
                parent, child, edge = node
                if type(protocol) == parent and p == edge:
                    return child

        return RAW.Header



    def rcheckprotocol(self, protocol):
        for node in self.tree:
            parent, child, edge = node

            if type(protocol) == child:
                prev = parent()
                prev.protocol = edge
                return prev



    def read(self, next=ETHERNET.Header):
        packet = self.packet
        self.layer = []

        while True:
            current = next
            protocol = current(packet)
            protocol.read()

            self.layer.append( protocol )

            if type(protocol) == RAW.Header: break

            packet = protocol.data
            next = self.checkprotocol( protocol )

        return len(self.layer)



    def fill(self, protocol, src=None, dst=None):
        if type( protocol ) == RAW.Header: return None
        self.layer = [RAW.Header()]

        while True:
            self.layer.insert( 0, protocol )
            protocol = self.rcheckprotocol( protocol )
            if not protocol: break

        for p in self.layer:
            if hasattr(p, "src") and src:
                p.src = src.copy()
            if hasattr(p, "dst") and dst:
                p.dst = dst.copy()

        return len(self.layer)



    def build(self):
        for i in range( len(self.layer) )[::-1]:
            self.layer[i].build()
            self.layer[i-1].data += self.layer[i].packet

        self.packet = self.layer[0].packet

        return len(self.packet)
