#!/usr/bin/env python
# coding: utf-8

from pythonosc import dispatcher
from pythonosc import osc_server 
#from pythonosc.osc_server import AsyncIOOSCUDPServer
#import asyncio

import time

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
	l_ear, l_forehead, r_forehead, r_ear = args
	unused_addr = []
	print("%s %f %f %f %f" % unused_addr, l_ear, l_forehead, r_forehead, r_ear)
	print(ch1)

if __name__ == "__main__":

	ip = "192.168.1.56"

	port = 63323


	dispatcher = dispatcher.Dispatcher()

	dispatcher.map("/Muse-EB72/eeg", eeg_handler, "EEG")

	server = osc_server.ThreadingOSCUDPServer(
	    (ip, port), dispatcher)

	print("Serving on {}".format(server.server_address))

	while True:
		server.handle_request()


