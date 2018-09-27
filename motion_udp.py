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

Tf = bpy.data.objects.get('Cube_1')
Tr = bpy.data.objects.get('Cube_2')
c = (Tf,Tr)
print('Blender initialized')


def read_udp(obj):
    while True:
        data,addr = sock.recvfrom(1024)
        d_unpk = struct.unpack('d'*14,data)
        print("msg:",d_unpk , "  addr:", addr)
        x_1 = d_unpk[0]
        y_1 = d_unpk[2]
        yaw_1 = d_unpk[4]
        x_2 = d_unpk[1]
        y_2 = d_unpk[3]
        yaw_2 = d_unpk[5]
        z_1 = d_unpk[12]
        z_2 = d_unpk[13]
        obj[0].location.x = x_1
        obj[0].location.y = y_1
        obj[0].location.z = z_1
        obj[0].rotation_euler[2] = yaw_1*pi/180
        obj[1].location.x = x_2
        obj[1].location.y = y_2
        obj[1].location.z = z_2
        obj[1].rotation_euler[2] = yaw_2*pi/180

t = threading.Thread(target = read_udp, args= (c,))

try:
    t.start()
except:
    print('threading error')


    


