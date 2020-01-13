#!/usr/bin/env python
# coding: utf-8

import socket
import DateTime
import time
import select


UDP_IP = "192.168.1.56" #UDP IP adress
UDP_PORT = 63323 #UDP port for osc stream


sock = socket.socket(socket.AF_INET,  # Internet
                   socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_PORT)) #binding the name to the socket

data = sock.recvfrom(1024) # receiving data from socket

while True:
    print(data)






