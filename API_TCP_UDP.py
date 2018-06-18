#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Authors: Juliani Schlickmann Damasceno
         Mateus Seenem Tavares
Description: This file contain functions developed to use in UDP connections.
'''
from socket import *
import random
import json
from time import time

class Package():
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

    def change_dictionary_value(self, dictionary, key_to_find, new_value):
        for key in dictionary.keys():
            if key == key_to_find:
                dictionary[key] = new_value
                break

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

class API_TCP_UDP():
    '''
        Constructor default
    '''
    def __init__(self):
        # General attributes
        self.socket = socket(AF_INET, SOCK_DGRAM)
        #self.socket.settimeout(30)
        self.window = []
        self.MTU = 1500
        self.slow_start = True
        self.cwnd = 1
        self.last_seq = 0
        self.last_ack = None
        self.RTT = None

    '''
        Function for the server to listen client's commands
    '''
    def server_listening(self, server_address, server_port):
        self.socket.bind((server_address, server_port))
        print ("\n****** The server is ready! ******\n")

        object_package = Package()

        while True:
            '''
                Here starts the handshake
            '''
            package_string, (client_address, client_port) = self.socket.recvfrom(self.MTU) #first touch between server and client
            object_package.package = json.loads(package_string)
            #print (object_package.package) #remove later

            if object_package.package['confirmation_number'] is None and object_package.package['sequence_number'] is None:
                #as the context changed, swaping origin and destination, and inserting the port used by client
                object_package.update_values({'origin_port': object_package.package['destination_port'], 'destination_port': client_port,
                                    'ACK': 1, 'rwnd': 65535})

                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                self.socket.sendto(package_string , (client_address, client_port))
                print ("SEGUNDA VIA CONEXÃO!\n\n") #remove later

                if object_package.package['flags']['ACK'] is not None:
                    package_string, (client_address, client_port) = self.socket.recvfrom(self.MTU) #third touch between server and client
                    object_package.package = json.loads(package_string)
                    print (object_package.package) #remove later

            elif object_package.package['flags']['FIN'] is not None:
                object_package.update_values({'origin_port': object_package.package['destination_port'], 'destination_port': client_port})
                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                print ("\nTERMINANDO CONEXÃO!\n") #remove later
                self.socket.sendto(package_string , (client_address, client_port))
                print ("\nConnection finished successfully!\n")
                self.socket.close()
                break

            else:
                object_package.update_values({'origin_port': object_package.package['destination_port'], 'destination_port': client_port,
                                        'confirmation_number': (object_package.package['sequence_number'] + len(object_package.package['data']))})

                self.last_ack =  object_package.package['confirmation_number']

                print('\nTeste alteração ACK e Sequence Number ********\n') #remove later
                print(json.dumps(object_package.package, sort_keys=True, indent=4)) #remove later
                print('\n**********************************************') #remove later

                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                self.socket.sendto(package_string , (client_address, client_port))

                '''
                    We must coding here functions such as send_data...
                    Start window...timeout... sampleRTT ... to control RWND and CWND...
                    look the sequence logic carefully and talk talk to me if necessary
                '''

    def connection(self, server_address, server_port):
        if str(server_address) == 'localhost':
            server_address = '127.0.0.1'

        object_package = Package()

        #beginning connection
        object_package.update_values({'destination_port': server_port,'SYN': 1})

        package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")

        self.socket.sendto(package_string , (server_address, server_port))
        print ("PRIMEIRA VIA CONEXÃO!\n\n") #remove later

        if object_package.package['flags']['SYN'] == 1:
            package_string, address = self.socket.recvfrom(self.MTU) #second touch between server and client #review this comment with Juliani
            object_package.package = json.loads(package_string)
            print (object_package.package) #remove later

            #as the context changed, swaping origin and destination
            object_package.update_values({'origin_port': object_package.package['destination_port'], 'destination_port': object_package.package['origin_port'], 'SYN': 0})

            package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
            print ("\nSending a package!\n\n")

            self.socket.sendto(package_string , (server_address, server_port))
            print ("TERCEIRA VIA CONEXÃO!\n\n") #remove later

            return (self.socket, (server_address, server_port)) #review the utility with Juliani...maybe

    def close_connection(self, connected):
        self.socket, (address, port) = connected

        object_package = Package()

        object_package.update_values({'FIN': 1})

        package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")

        self.socket.sendto(package_string, (address, port))

        package_string, (address, port) = self.socket.recvfrom(self.MTU) #second touch between server and client

        object_package.package = json.loads(package_string)

        print (object_package.package) #remove later

        if object_package.package['flags']['FIN'] == 1:
            print ("\nTERMINANDO CONEXÃO!\n") #remove later
            print ("\nConnection finished successfully!\n")
            self.socket.close()
        else:
            print ("\nSomething is wrong. The connection was not closed.\n")

    def send_data(self, aData, connected):
        self.socket, (address, port) = connected
        segment = 0
        number_segment = -1

        for item in aData:
            print (item) #remove later
            temp = item
            while len(temp) > 10: #depois trocar 10 por 1460 (MSS)
                variavel = temp[0:10] #depois trocar 10 por 1460 (MSS)
                number_segment = number_segment + 1
                temp = temp.replace(variavel, "")
                self.create_package(variavel, number_segment) #create segment
                #break #remove later

            if temp is not None:
                number_segment = number_segment + 1
                self.create_package(temp, number_segment)

        #verify if window is empty
        if self.window is None:
            print ('\nThe window is empty. \n')
        else:
            while self.slow_start: #PRECISAMOS IMPLEMENTAR O SLOW START. PRECISA IMPLEMENTAR O RECEBIMENTO DAS RESPOSTAS DO SERVER...
                if segment < len(self.window):
                    for i in range(self.cwnd):
                        print ("\nSending a package!\n\n")
                        self.socket.sendto(self.window[segment] , (address, port))
                        self.RTT = time()
                        segment = segment + 1
                else:
                    for i in range(self.cwnd):
                        package_string, (address, port) = self.socket.recvfrom(self.MTU)

                        print('\n**********************************************\n') #remove later
                        print(package_string)
                        print('\n**********************************************\n') #remove later


                    self.cwnd = self.cwnd * 2 #this didn't supose to be in the if block? or while block?

    def create_package(self, aData, number_segment):
        object_package = Package() 
        
        self.last_seq =  self.getting_sequence_number()

        object_package.update_values({'ACK': 0, 'sequence_number': self.last_seq, 'data': aData })

        package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
        self._window(package_string)

    def _window(self, package):

        self.window.append(package)

        print ('MINHA JANELA') #remove later
        for a in self.window: #remove later
            print (a) #remove later

    def getting_sequence_number(self):
        seq = 0

        if len(self.window) > 0:        
            package = json.loads(self.window[-1])
            seq = package['sequence_number'] + len(package['data'])

        return seq

        '''
            Aqui temos que ver se o array de dados vindo do client ultrapassa o MTU...(1500)
            Ultrapassando... deverá ser segmentado os dados... dai que entram os pacotes e a janela...
            a janela é uma lista de pacotes... e aqui se faz importante o numero de sequencia ao segmentar os dados...

            a partir do envio do primeiro pacote devemos começar a calcular o RTT (estimativa de ida e volta)
            no livro é citado o sampleRTT (esse NAO DEVE ser calculado para segmentos retransmitidos.)
            procurar por estimatedRTT (tem uma fórmula específica)


            devemos inserir timeout... entre outros controles
        '''
