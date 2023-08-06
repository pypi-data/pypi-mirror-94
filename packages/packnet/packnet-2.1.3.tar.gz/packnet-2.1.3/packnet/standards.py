"""

 PACKNET  -  c0mplh4cks

 STANDARDS


"""





# === Importing Dependencies === #
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack
from .vendor import vendors







# === Get Public IP === #
def getpublicip():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("ifconfig.me", 80))
    s.send( b"GET http://ifconfig.me HTTP/1.1\r\n\r\n" )
    data = s.recv(1024).decode()

    return data.split("\r\n\r\n")[1]





# === Mac Vendor Lookup === #
def maclookup(mac):
    mac = mac.upper().replace(":", "")

    vendor = vendors.get(mac[:6])
    if not vendor:
        vendor = "Unknown vendor"

    return vendor





# === Encode === #
class encode:
    def ip(ip):
        return b"".join( [pack(">B", int(n)) for n in ip.split(".")] )


    def ipv6(ip):
        ip = ip.split(":")

        if "" in ip:
            n = ip.index("")
            for i in range( 9-len(ip) ):
                ip.insert(n, "0")
            ip.remove("")

        return b"".join([ pack(">H", int(i, 16)) for i in ip ])


    def mac(mac):
        return b"".join( [pack(">B", int(n, 16)) for n in mac.split(":")] )


    def tobyte(v):
        b = bin(v)[2:]
        while len(b) % 8 != 0:
            b = "0" + b
        return b"".join([ pack(">B", int(b[i:i+8], 2)) for i in range(0, len(b), 8) ])


    def name(name, header=b""):
        encoded = b""
        for label in f"{ name }.".split("."):
            encoded += ( pack(">B", len(label)) + label.encode() )

        pointer = header.find(encoded)
        if pointer == -1:
            return encoded
        else:
            return pack(">H", 49152+pointer )







# === Decode === #
class decode:
    def ip(ip):
        return ".".join( [str(n) for n in ip] )


    def ipv6(ip):
        parts = [ ip[i:i+2] for i in range(0, len(ip), 2) ]
        parts = [ hex(unpack(">H", p)[0])[2:] for p in parts ]
        ip = ":".join(parts)
        for i in range(6, 0, -1):
            z = ":0" * i
            if z in ip:
                return ip.replace(z, ":", 1)
        return ip


    def mac(mac):
        return ":".join( ["{:02x}".format(n) for n in mac] )


    def toint(b):
        return sum([ i << (8*n) for n, i in enumerate(b[::-1]) ])


    def name(name, header=b"", ti=0):
        labels = []
        i = 0

        while True:
            length = name[i]

            if length == 0:
                i += 1
                break

            elif (length >> 6) == 3:
                pointer = unpack(">H", name[i:i+2] )[0] -49152
                i += 2
                labels.append( decode.name( header[pointer:], header )[1] )
                break

            else:
                i += 1
                labels.append( name[ i:length+i ].decode() )
                i += length

        name = ".".join( labels )

        return i+ti, name







# === Checksum === #
def checksum(header):
        header = b"".join(header)

        if (len(header) %2) != 0:
            header += b"\x00"

        values = unpack( f">{ len(header)//2 }H", header )
        n = sum(values) %65535
        n = 65535-n

        return pack(">H", n )
