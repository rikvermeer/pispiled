import socket, json

UDP_IP = "192.168.2.255"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))

from numpy import *
from numpy.random import permutation

spidev = file('/dev/spidev0.0', 'wb')
gamma = array([0x80 | int( (i / 255.0) ** 2.5 * 127 + .5 ) for i in range(256)])

set_R = {"segments":32, "waves":1, "amp":128, "off_x":0, "off_y":128}
set_G = {"segments":32, "waves":1, "amp":128, "off_x":8, "off_y":128}
set_B = {"segments":32, "waves":1, "amp":0, "off_x":16, "off_y":0}

def getSine(settings):
    amount = settings["segments"]
    waves = settings["waves"]
    amp = settings["amp"]
    off_x = settings["off_x"]
    off_y = settings["off_y"]
    
    rads, step = linspace( 0, 2*pi*waves, amount, retstep=True)
    rads = rads + (step * off_x)
    result = int8(sin(rads) * amp)
    result = result + off_y
    return result

aR = getSine(set_R)
aG = getSine(set_G)
aB = getSine(set_B)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    js =  json.loads(data)
    
    if( len(js[0]) > 0):
        for a in js[0]:
            set_R[a] = js[0][a]
        aR = getSine(set_R)
        
    if( len(js[1]) > 0):
        for a in js[1]:
            set_G[a] = js[1][a]
        aG = getSine(set_G)

    if( len(js[2]) > 0):
        for a in js[2]:
            set_B[a] = js[2][a]
        aB = getSine(set_B)
        
    bytes = clip(array([aG, aR, aB]), 0, 255)
    bytes = gamma[bytes]
    bytes = bytes.flatten('F')

    bts = bytearray(3 * 32 + 1)
    for i in range(32):
        i *= 3
        bts[i] = bytes[i]
        bts[i+1] = bytes[i+1]
        bts[i+2] = bytes[i+2]
    bts[96] = 0

    spidev.write(bts)
    spidev.flush()