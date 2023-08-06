"""

 PACKNET  -  c0mplh4cks

 PACKAGER


"""





# === Importing Dependencies === #
from .tree import Tree
from . import ETHERNET
from . import RAW







# === Packager === #
class Packager():
    def __init__(self, packet=b""):
        self.packet = packet

        self.layer = []



    def checkprotocol(self, protocol):
        if protocol.protocol == None: return RAW.Header

        l = protocol.protocol
        l = [l] if type(l) == int else l

        for p in list(l):
            child = Tree().get( parent=type(protocol), edge=protocol.protocol )
            if child: return child

        return RAW.Header



    def rcheckprotocol(self, protocol):
        nodes = Tree().getnodes( child=type(protocol) )
        
        if nodes:
            parent, child, edge = nodes[0]
            result = parent()
            result.protocol = edge

            return result



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
