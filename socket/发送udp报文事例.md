例子1：
```python
from socket import *
import struct
import time

def testScan():
    data = [0x02,0x80, 0, 0 ,0,0xcc,0x70,0x02020209,0x03,0x03,''.encode(),'bbbd'.encode()]
    buffer = struct.pack("!HHIIIHHIII32s64s", *data)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    sendAddr = ("10.24.123.105", 9502)#"192.168.37.13"
    udpSocket.sendto(buffer, sendAddr)
    udpSocket.close()

def testMomit():
    data = [0x02,0x80, 0, 0 ,0,0xc9,0x70]#报文头
    data.append(0x04)
    data.append(0x03)
    data.append(0x00)
    data.append(0x04)
    data.append(0x06)
    data.append(0x02020209)
    data.append(0x02020210)
    data.append(0xCA)
    data.append(0xCCCC)
    data.append(0x04)
    data.append(int(time.time()))
    data.append(0x14)
    data.append(0x0202020902020209)
    data.append(0x00)
    data.append(0x00)
    data.append(0x00)
    data.append(0x00)
    buffer = struct.pack("!HHIIIHH IIHBBIIIIIIIQQQQQ", *data)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    sendAddr = ("10.24.123.105", 9502)#"192.168.37.13"
    udpSocket.sendto(buffer, sendAddr)
    udpSocket.close()

if __name__ == "__main__":
    testScan()
    testMomit()
```

例子2：
```python
import struct
from scapy.all import *

data = [0x02,0x80, 0, 0 ,0,0xcc,0x70,0x02020209,0x03,0x03,''.encode(),'bbbd'.encode()]
buffer = struct.pack("!HHIIIHHIII32s64s", *data)
pkt = IP(src='10.24.40.45', dst='10.24.41.168')/UDP(sport=12345, dport=9502)/buffer
send(pkt, inter=1, count=1)


data = [0x02,0x64,0x5bf4d554, 0x0027df6d ,0x0a18282d,0xc9,0x54]#报文头
data.append(0x04)
data.append(0x03)
data.append(0x0000)
data.append(0x04)
data.append(0x11)
data.append(0x2828001c)
data.append(0x32320002)
data.append(0x00000400)
data.append(0x00000400)
data.append(0x3000000a)
data.append(int(time.time()))#
data.append(0x0000035d)
data.append(0x00209400001b12ac)
data.append(''.encode())
buffer = struct.pack("!HHIIIHHIIHBBIIIIIIIQ32s", *data)
pkt = IP(src='10.24.40.45', dst='10.24.41.168')/UDP(sport=9501, dport=9502)/buffer
send(pkt)
```