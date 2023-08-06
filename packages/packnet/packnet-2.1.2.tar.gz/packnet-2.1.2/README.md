# PACKNET
*Hacked together into entirety by c0mplh4cks*

____


## About

This package is created to build low-level networking packets which can be used when building various types of applications. Using this package, it is possible to make packets ranging from OSI model level 2 to level 7. One of the endless applications could be a network device discovery tool using the address resolution protocol for example. Apart from only building numerous headers and payloads, this package makes it also possible to read received data and extract useful information, making it possible to interact with a Python script.


____


## Table of Contents
* [OSI model](#osi-model)
* [Installation](#installation)
  1. [PyPi](#installation-from-pypi)
  2. [GitHub](#installation-from-github)
* [Importing packnet](#import)
* [Building packets](#building)
  1. [ARP request](#arp-request-encode)
  2. [TCP message](#tcp-message-encode)
  3. [UDP message](#udp-message-encode)
  4. [DNS query](#dns-query-encode)
* [Reading packets](#reading)
  1. [ARP](#arp-decode)
  2. [TCP](#tcp-decode)
  3. [DNS](#dns-decode)
* [RAW Header](#raw-header)
* [Interface](#interface)
* [Packager](#packager)
  1. [Reading packets](#reading-packets-using-packager)
  2. [Building packets](#building-packets-using-packager)


____


## OSI model

Open Systems Interconnection model


No | Layer        | Function                    | Protocol *(included in package)*
---|--------------|-----------------------------|------------------------------
7  | Application  | Application communication   | DNS, MQTT
6  | Presentation | Representation & Encryption |
5  | Session      | Interhost communication     |
4  | Transport    | Connections & QoS           | TCP, UDP
3  | Network      | IP                          | IPv4, IPv6, ICMP, ICMPv6, ARP
2  | Data Link    | MAC                         | Ethernet
1  | Physical     | Bits                        |


Introduced to standardize networking protocols, allowing multiple networking devices from different developers to communicate among each other. The model consists of multiple layers with its own unique function. The OSI model differs from the TCP/IP model since it contains the presentation and session layers.


____


## Installation

The following will show how this package can be installed.


### Installation from PyPi

Install package by using `pip`:
```
pip3 install packnet
```
or
```
pip install packnet
```


### Installation from Github

Clone the repository:
```
git clone https://github.com/c0mplh4cks/packnet
```

Move inside the directory:
```
cd packnet
```

Install the library by running the following command:
```
pip3 install .
```
or
```
pip install .
```


____


## Import

Packages can be imported using different methods in Python. The following examples will show how this package can be imported and used in numerous ways.  
*(Note that the first and third examples are preferred)*
```python
import packnet  # Imports everything inside the package.

packnet.standards.maclookup("00:00:00:00:00:00")
packnet.standards.encode.ip("127.0.0.1")
interface = packnet.Interface()
ethernet_header = packnet.ETHERNET.Header()
dns_query = packnet.DNS.Query()
```

```python
from packnet import * # Imports everything inside the package. NOT RECOMMENDED!

standards.maclookup("00:00:00:00:00:00")
standards.encode.ip("127.0.0.1")
interface = Interface()
ethernet_header = ETHERNET.Header()
dns_query = DNS.Query()
```

```python
from packnet import standards, Interface, ETHERNET, DNS   # Imports specific modules/objects/functions from package.

standards.maclookup("00:00:00:00:00:00")
standards.encode.ip("127.0.0.1")
interface = Interface()
ethernet_header = ETHERNET.Header()
dns_query = DNS.Query()
```


____


## Building

The following snippets of code will serve as an example when building different types of packets.


### ARP request encode

```python
from packnet import ETHERNET, ARP   # importing ETHERNET and ARP objects


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]


arp = ARP.Header()    # defining ARP Header object
arp.src = src         # setting source address
arp.dst = dst         # setting destination address
arp.op = 1            # setting operation code to 1(request)
arp.build()           # building ARP Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0806    # setting protocol 0x0806(ARP)
ethernet.data = arp.packet    # adding ARP Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build ARP request including ethernet header
```


### TCP message encode

```python
from packnet import ETHERNET, IPv4, TCP


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]

msg = "hello".encode()      # defining TCP payload

tcp = TCP.Header()    # defining TCP Header object
tcp.src = src         # setting source address
tcp.dst = dst         # setting destination address
tcp.seq = 1234        # setting sequence number
tcp.ack = 4321        # setting acknowledgment number
tcp.data = msg        # setting payload
tcp.build()           # building TCP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.id = 31415         # setting identifier
ipv4.protocol = 6       # setting protocol 6(TCP)
ipv4.data = tcp.packet  # adding TCP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers
```


### UDP message encode

```python
from packnet import ETHERNET, IPv4, UDP


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]

msg = "hello".encode()      # defining UDP payload


udp = UDP.Header()    # defining UDP Header object
udp.src = src         # setting source address
udp.dst = dst         # setting destination address
udp.data = msg        # setting payload
udp.build()           # building UDP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.id = 1234          # setting identifier
ipv4.protocol = 17      # setting protocol 17(UDP)
ipv4.data = udp.packet  # adding UDP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers

```


### DNS query encode

```python
from packnet import ETHERNET, IPv4, UDP, DNS


src = ["1.1.1.1", 0, "11:11:11:11:11:11"]   # defining source address ["IP", PORT, "MAC"]
dst = ["2.2.2.2", 0, "22:22:22:22:22:22"]   # defining source address ["IP", PORT, "MAC"]


query = DNS.Query()         # defining DNS Query object
query.name = "github.com"   # setting name to be resolved

dns = DNS.Header()          # defining DNS Header object
dns.id = 1234               # setting identifier
dns.question.append(query)  # adding query to header
dns.build()                 # building DNS Header

udp = UDP.Header()      # defining UDP Header object
udp.src = src           # setting source address
udp.dst = dst           # setting destination address
udp.data = dns.packet   # adding DNS Header
udp.build()             # building UDP Header

ipv4 = IPv4.Header()    # defining IPv4 Header object
ipv4.src = src          # setting source address
ipv4.dst = dst          # setting destination address
ipv4.protocol = 17      # setting protocol 17(UDP)
ipv4.data = udp.packet  # adding UDP Header
ipv4.build()            # building IPv4 Header

ethernet = ETHERNET.Header()  # defining ETHERNET Header object
ethernet.src = src            # setting source address
ethernet.dst = dst            # setting destination address
ethernet.protocol = 0x0800    # setting protocol 0x0800(IPv4)
ethernet.data = ipv4.packet   # adding IPv4 Header
ethernet.build()              # building ETHERNET Header

print(ethernet.packet)    # printing build UDP packet including IPv4 and ETHERNET headers
```


____


## Reading

The following snippets of code will serve as an example when reading various types of packets and requiring the information.


### ARP decode

```python
from packnet import ETHERNET, ARP


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x06\x00\x01\x08\x00\x06\x04\x00\x02\x11\x11\x11\x11\x11\x11\x01\x01\x01\x01""""""\x02\x02\x02\x02'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0806:     # check if packet contains an ARP Header
  arp = ARP.Header(ethernet.data)   # defining ARP Header object & parsing encoded data
  arp.read()                        # reading ARP Header

  print( "ARP HEADER" )             # displaying acquired data
  print( f" length    { arp.length }" )
  print( f" source    { arp.src }" )
  print( f" target    { arp.dst }" )
  print( f" operation { arp.op }" )
  print()
```


### TCP decode

```python
from packnet import ETHERNET, IPv4, TCP


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x00E\x00\x00(z\xb7@\x00@\x06\xba\x13\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x04\xd2\x00\x00\x10\xe1P\x00\xfd\xe8\x96C\x00\x00hello'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0800:     # check if packet contains an IPv4 Header
  ipv4 = IPv4.Header(ethernet.data) # defining IPv4 Header object & parsing encoded data
  ipv4.read()                       # reading IPv4 Header

  print( "IPv4 HEADER" )            # displaying acquired data
  print( f" length   { ipv4.length }" )
  print( f" source   { ipv4.src }" )
  print( f" target   { ipv4.dst }" )
  print( f" id       { ipv4.id }" )
  print( f" protocol { ipv4.protocol }" )
  print()


  if ipv4.protocol == 6:          # check if packet contains an TCP Header
    tcp = TCP.Header(ipv4.data)   # defining TCP Header object & parsing encoded data
    tcp.read()                    # reading TCP Header

    print( "TCP HEADER" )         # displaying acquired data
    print( f" length                 { tcp.length }" )
    print( f" source                 { tcp.src }" )
    print( f" target                 { tcp.dst }" )
    print( f" sequence number        { tcp.seq }" )
    print( f" acknowledgement number { tcp.ack }" )
    for option in tcp.options:
      print( f" option kind { option.kind }" )
    print( f"data { tcp.data }" )
    print()

```


### DNS decode

```python
from packnet import ETHERNET, IPv4, UDP, DNS


packet = b'""""""\x11\x11\x11\x11\x11\x11\x08\x00E\x00\x008\x00\x00@\x00@\x114\xb0\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00$\xe9\xc3\x04\xd2\x00@\x00\x01\x00\x00\x00\x00\x00\x00\x06github\x03com\x00\x00\x05\x00\x01'
# ^ packet which must be decoded


ethernet = ETHERNET.Header(packet)    # defining ETHERNET Header object & parsing encoded packet
ethernet.read()                       # reading ETHERNET Header

print( "ETHERNET HEADER" )            # displaying acquired data
print( f" length   { ethernet.length }" )
print( f" source   { ethernet.src }" )
print( f" target   { ethernet.dst }" )
print( f" protocol { ethernet.protocol }" )
print()


if ethernet.protocol == 0x0800:     # check if packet contains an IPv4 Header
  ipv4 = IPv4.Header(ethernet.data) # defining IPv4 Header object & parsing encoded data
  ipv4.read()                       # reading IPv4 Header

  print( "IPv4 HEADER" )            # displaying acquired data
  print( f"length    { ipv4.length }" )
  print( f" source   { ipv4.src }" )
  print( f" target   { ipv4.dst }" )
  print( f" protocol { ipv4.protocol }" )
  print( f" id       { ipv4.id }" )
  print()


  if ipv4.protocol == 17:         # check if packet contains an UDP Header
    udp = UDP.Header(ipv4.data)   # defining UDP Header object & parsing encoded data
    udp.read()                    # reading UDP Header

    print( "UDP HEADER" )         # displaying acquired data
    print( f" length { udp.length }" )
    print( f" source { udp.src }" )
    print( f" target { udp.dst }" )
    print()


    dns = DNS.Header(udp.data)  # defining DNS Header object & parsing encoded data
    dns.read()                  # reading DNS Header

    print( "DNS HEADER" )         # displaying acquired data
    print( f" id { dns.id }" )
    print( f" questions      { len(dns.question) }" )
    print( f" answer RRs     { len(dns.answer) }" )
    print( f" authority RRs  { len(dns.authority) }" )
    print( f" additional RRs { len(dns.additional) }" )
    print()

    for question in dns.question:
      print( "DNS QUERY" )         # displaying acquired data
      print( f"name   { question.name }" )
      print( f"type   { question.type }" )
      print( f"classs { question.classif }" )
      print()

    for answer in dns.answer:
      print( "DNS ANSWER" )         # displaying acquired data
      print( f"name   { answer.name }" )
      print( f"type   { answer.type }" )
      print( f"classs { answer.classif }" )
      print( f"ttl    { answer.ttl }" )
      print( f"cname  { answer.cname }" )
      print()
```


____


## RAW Header

The RAW module is a special module created for a specific but simple reason. It contains raw data which is not decodable by the currently implemented protocols. `RAW.Header` can be used in the same way as the other protocols since it contains the `build` and `read` functions. The only two attributes which are usefull for implementations, are the `data` and `length` attributes. The `data` attribute contains the undecodable data in bytes. The `length` attribute contains the length of the data in bytes.



____


## Interface

Interface is a special module which can be used for creating low-level sockets and automatically requiring address information from the specified interface. Below an example for a use case.  
**Requires `sudo` rights!**

```python
from packnet import Interface


interface = Interface(card="eth0", port=0, passive=False)

print(interface.addr)

interface.send(b"hello")
print(interface.recv())
```

It is alse possible to require a MAC address from a device using the following function:

```python
import packnet

interface = packnet.Interface()
ip, port, mac = interface.getmac("192.168.1.1")

print(mac)
```


____


## Packager

The Packager module automates the process of building and reading networking packets.


### Reading packets using Packager

The following example shows how it is possible to use the Packager class to automatically analyse the different layers of the incoming packet. The example parses the incoming packet into a Packager object and filtering to finally display the requested name of the DNS query.

```python
import packnet

interface = packnet.Interface()

while True:
  packet, info = interface.recv()

  package = packnet.Packager(packet)
  package.read()

  # Filtering for DNS Queries
  if len( package.layer ) < 4: continue
  if type( package.layer[3] ) != packnet.DNS.Header: continue
  if len( package.layer[3].answer ) != 0: continue
  if len( package.layer[3].question ) != 0: continue
  if package.layer[3].question[0].type != 1: continue

  print( package.layer[3].question[0].name )
```


### Building packets using Packager

The following snippet of code describes how Packager automatically completes the required underlying protocols.

```python
import packnet

package = packnet.Packager()
package.build( packnet.UDP.Header() )   # building a UDP packet

print( package.layer )  # the printed list contains objects for every required protocol
```
