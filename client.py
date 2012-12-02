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
    js =  json.loads(data)
    bytes = clip(array([js["R"], js["G"], js["B"]]), 0, 255)
    bytes = gamma[bytes]
    bytes = bytes.flatten('F')
    
    bts = bytearray(3 * 32 + 1)
    for i in range(32):
        i *= 3
        bts[i] = bytes[i]
        bts[i+1] = bytes[i+1]
        bts[i+2] = bytes[i+2]
    bts[96] = 0
    
    spidev.write(data)
    spidev.flush()
