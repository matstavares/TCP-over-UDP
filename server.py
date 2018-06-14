#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from API_TCP_UDP import *

object_server = API_TCP_UDP()

'''server_IP = raw_input("Insert the server IP: ")

while True:
    try:
        server_port = input("Insert the server port: ")
        break
    except:
        print ("You must to inform a integer number!\n")'''

object_server.server_listening('localhost', 12000)
