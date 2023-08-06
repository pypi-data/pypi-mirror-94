"""

 PACKNET  -  c0mplh4cks

 TREE


"""





# === Importing Dependencies === #
from . import ETHERNET
from . import IPv4, ARP
from . import ICMP, UDP, TCP
from . import MQTT, DNS







# === Tree === #
class Tree:
    def __init__(self):
        self.nodes = [
            [ ETHERNET.Header, IPv4.Header, 0x0800 ],
            [ ETHERNET.Header, ARP.Header, 0x0806 ],
            [ IPv4.Header, ICMP.Header, 1 ],
            [ IPv4.Header, UDP.Header, 17 ],
            [ IPv4.Header, TCP.Header, 6 ],
            [ UDP.Header, DNS.Header, 53 ],
            [ TCP.Header, MQTT.Header, 1883 ],
        ]



    def get(self, parent=None, child=None, edge=None):
        for node in self.nodes:
            p, c, e = node
            result = [p==parent, c==child, e==edge]
            if result.count(True) == 2:
                return node[ result.index(False) ]



    def getnodes(self, parent=None, child=None, edge=None):
        out = []
        
        for node in self.nodes:
            p, c, e = node
            result = [p==parent, c==child, e==edge]

            if True in result:
                out.append(node)

        return out
