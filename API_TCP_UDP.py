#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Authors: Juliani Schlickmann Damasceno
         Mateus Seenem Tavares
Description: This file contain functions developed to use in UDP connectionself.
'''
from socket import *
import random
import json
from time import time

class API_TCP_UDP():
    '''
        Constructor default
    '''
    def __init__(self):
        # header TCP attributes -------- segments header
        self.package = {}
        self.package['origin_port'] = None
        self.package['destination_port'] = None
        self.package['sequence_number'] = None
        self.package['confirmation_number'] = None #it's a ACK
        self.package['length_header'] = None
        self.package['flags'] = { 'ACK': None, 'SYN': None, 'FIN': None }  #dictionary (it's look like a json ['key': value])
        self.package['data'] = ""
        self.package['rwnd'] = None #receiver window

        # General attributes
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(30)
        self.window = {}
        self.MTU = 1500

    '''
        Function for the server to listen client's commands
    '''
    def server_listening(self, server_address, server_port):
        self.socket.bind((server_address, server_port))
        print ("\n****** The server is ready! ******\n")

        while True:
            '''
                Here starts the handshake
            '''
            if self.package['confirmation_number'] is None:
                package_string, (client_address, client_port) = self.receivingFrom(self.MTU) #first touch between server and client


                self.package = json.loads(package_string)

                print (self.package) #remove later

                self.update_values({'origin_port': self.package['destination_port'], 'destination_port': client_port,
                                    'ACK': 1, 'rwnd': 65535})

                package_string = json.dumps(self.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                self.sendingTo(package_string , (client_address, client_port))
                print ("SEGUNDA VIA CONEXÃO!\n\n") #remove later

                if self.package['flags']['ACK'] is not None:
                    package_string, (client_address, client_port) = self.receivingFrom(self.MTU) #third touch between server and client

                    self.package = json.loads(package_string)

                    print (self.package) #remove later

            else:
                package_string, (client_address, client_port) = self.receivingFrom(self.MTU) #third touch between server and client

                self.package = json.loads(package_string)

                if self.package['flags']['FIN'] is not None:

                    self.update_values({'origin_port': self.package['destination_port'], 'destination_port': client_port})

                    package_string = json.dumps(self.package, sort_keys=True, indent=4)
                    print ("\nSending a package!\n\n")

                    print ("\nTERMINANDO CONEXÃO!\n") #remove later
                    self.sendingTo(package_string , (client_address, client_port))
                    print ("\nConnection finished successfully!\n")
                    self.socket.close()
                    break

                '''
                    We must coding here functions such as send_data...
                    Start window...timeout... sampleRTT ... to control RWND and CWND...
                    look the sequence logic carefully and talk talk to me if necessary
                '''

    def connection(self, server_address, server_port):
        if str(server_address) == 'localhost':
            server_address = '127.0.0.1'

        #beginning connection
        self.update_values({'destination_port': server_port,'SYN': 1})

        package_string = json.dumps(self.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")

        self.sendingTo(package_string, (server_address, server_port))
        print ("PRIMEIRA VIA CONEXÃO!\n\n") #remove later

        if self.package['flags']['SYN'] == 1:
            package_string, address = self.receivingFrom(self.MTU) #second touch between server and client

            self.package = json.loads(package_string)

            print (self.package) #remove later

            self.update_values({'origin_port': self.package['destination_port'], 'destination_port': self.package['origin_port'],
                                'SYN': 0})

            package_string = json.dumps(self.package, sort_keys=True, indent=4)
            print ("\nSending a package!\n\n")

            self.sendingTo(package_string , (server_address, server_port))
            print ("TERCEIRA VIA CONEXÃO!\n\n") #remove later

            return (self.socket, (server_address, server_port))


    def change_dictionary_value(self, dictionary, key_to_find, new_value):
        for key in dictionary.keys():
            if key == key_to_find:
                dictionary[key] = new_value

    '''
        This function is the main point to change values in our application.
        It receive a dic (key: value), notice that is the new value.
    '''
    def update_values(self, aKeys):
        for key,val in aKeys.items():
            if key == 'SYN' or key == 'ACK' or key == 'FIN':
                self.change_dictionary_value(self.package['flags'], key, val)
            else:
                self.change_dictionary_value(self.package, key, val)

    def close_connection(self, connected):
        self.socket, (address, port) = connected

        self.update_values({'FIN': 1})

        package_string = json.dumps(self.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")

        self.sendingTo(package_string, (address, port))

        package_string, (address, port) = self.receivingFrom(self.MTU) #second touch between server and client

        self.package = json.loads(package_string)

        print (self.package) #remove later

        if self.package['flags']['FIN'] == 1:
            print ("\nTERMINANDO CONEXÃO!\n") #remove later
            print ("\nConnection finished successfully!\n")
            self.socket.close()
        else:
            print ("\nSomething is wrong. The connection was not closed.\n")

    def send_data(self, aData, connected):
        self.socket, (address, port) = connected

        while len(aData) > self.MTU:
            print("")
            #quebrar os dados em até 1460 (MSS)
            #chamar função que cria packge passando o dado segmentado...

    #wrappers to encode and decode strings to bytes, to be sent/receive from socket
    def sendingTo(self, package_string, fulladdress):
        self.socket.sendto(package_string.encode(),fulladdress)

    def receivingFrom(self,mtu):
        package_string, address = self.socket.recvfrom(mtu)
        return (package_string.decode(), address)

    def create_package(self, aData):
        self.package = self.update_values({'data': aData})
        print (package)

        #alimentar self.window que deverá ser nossa janela de segmentos... no caso... temos que criar uma lista de pacotes...
        #se quiser criar uma nova funcao... fica a vontade....

        '''
            Aqui temos que ver se o array de dados vindo do client ultrapassa o MTU...(1500)
            Ultrapassando... deverá ser segmentado os dados... dai que entram os pacotes e a janela...
            a janela é uma lista de pacotes... e aqui se faz importante o numero de sequencia ao segmentar os dados...

            a partir do envio do primeiro pacote devemos começar a calcular o RTT (estimativa de ida e volta)
            no livro é citado o sampleRTT (esse NAO DEVE ser calculado para segmentos retransmitidos.)
            procurar por estimatedRTT (tem uma fórmula específica)


            devemos inserir timeout... entre outros controles
        '''
