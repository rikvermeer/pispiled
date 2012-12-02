import socket, json
from numpy import *
from numpy.random import permutation

UDP_IP = "192.168.137.255"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))


spidev = file('/dev/spidev0.0', 'wb')
gamma = array([0x80 | int( (i / 255.0) ** 2.5 * 127 + .5 ) for i in range(256)])

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
<<<<<<< HEAD
    #print data
    #js =  fromiter(json.loads(data), byte)
    js = json.loads(data)
    bytes = clip(array([js[0], js[1], js[2]]), 0, 255)
    #print bytes
=======
    js =  json.loads(data)
    bytes = clip(array([js[0][0], js[0][1], js[0][2]]), 0, 255)
>>>>>>> 2463aadd4462cd4398577ee30858036e152af5c1
    bytes = gamma[bytes]
    bytes = bytes.flatten('F')
    
    bts = bytearray(len(bytes) + 1)
    #print len(bytes)
    #print bytes
    for i in range(len(bytes)):
	print i, bytes[i]
        bts[i] = bytes[i]
    bts[len(bytes)] = 0
    #print bts
    spidev.write(bts)
    spidev.flush()
