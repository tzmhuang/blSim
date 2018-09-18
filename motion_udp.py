import bpy
import socket
import numpy as np
import time
#import matplotlib.pyplot as plt

import sys
dir = 'C:\\Users\\tom\\Desktop\\blSim'
sys.path.append(dir)

import struct
import threading
from gen_curve_2 import *


print('Initializing UDP socket...')
UDP_IP = "127.0.0.1"
UDP_PORT = 25000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
print ('Socket initialized')


print('Initializing Blender...')
try:
    draw()
except:
    print('error init. road')

c = bpy.data.objects.get('Cube')
print('Blender initialized')


def read_udp(obj):
    while True:
        data,addr = sock.recvfrom(1024)
        d_unpk = struct.unpack('d'*12,data)
        print("msg:",d_unpk , "  addr:", addr)
        x = d_unpk[0]
        y = d_unpk[2]
        obj.location.x = x
        obj.location.y = y

t = threading.Thread(target = read_udp, args= (c,))

try:
    t.start()
except:
    print('threading error')


    


