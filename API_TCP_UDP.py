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
import time

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
        self.package['rwnd'] = 65535 #receiver window

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
        # self.socket.settimeout(30)
        self.window = []
        self.toRTT = {} #time-out of RTT
        self.sampleRTT = 0
        self.timeout = 0.5
        self.MSS = 1204
        self.MTU = 1480 #udp header
        self.buffer = 4096
        self.slow_start = True
        self.cwnd = 1
        self.last_seq = 0
        self.last_ack = None
        self.duploAck = False
        self.triploAck = False

    '''
        Function for the server to listen client's commands
    '''
    def server_listening(self, server_address, server_port):
        self.socket.bind((server_address, server_port))
        print ("\n****** The server is ready! ******\n")
        test = True #remove later
        testao = True #remove later
        object_package = Package()

        while True:
            '''
                Here starts the handshake
            '''
            if test: #remove later
                test = False
                package_string, (client_address, client_port) = self.socket.recvfrom(self.buffer) #first touch between server and client
            else:
                package_string, (client_address, client_port) = self.socket.recvfrom(self.buffer) #first touch between server and client
                if testao:
                    testao = False
                else:
                    testao = True
                    test = True
                    continue
            object_package.package = json.loads(package_string)

            #as the context changed, swaping origin and destination, and inserting the port used by client
            object_package.update_values({'origin_port': object_package.package['destination_port'], 'destination_port': client_port})

            if object_package.package['confirmation_number'] is None and object_package.package['sequence_number'] is None:
                object_package.update_values({'ACK': 1, 'rwnd': 65535})

                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)

                object_package.update_values({'length_header': len(package_string) - len(object_package.package['data'])})

                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)

                print ("\nSending a package!\n\n")
                self.socket.sendto(package_string, (client_address, client_port))

                package_string, (client_address, client_port) = self.socket.recvfrom(self.buffer) #third touch between server and client
                object_package.package = json.loads(package_string)
                print (object_package.package) #remove later

            elif object_package.package['flags']['FIN'] is not None:
                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                self.socket.sendto(package_string , (client_address, client_port))
                self.socket.close()
                print ("\nConnection finished successfully!\n")
                break

            else:
                print('tamanho pacote: '+str(len(package_string))) #remove later
                print('tamanho dados: '+str(len(object_package.package['data']))) #remove later

                object_package.update_values({'confirmation_number': (object_package.package['sequence_number'] + len(object_package.package['data']))})

                self.last_seq = self.getting_sequence_number()

                self._window(object_package.package)

                self.verifyTripleAck(object_package, (client_address, client_port))

                self.last_ack =  self.getting_last_ack()

                if not self.verify_next_package_sequence(self.last_ack):
                    self.toRTT[self.last_ack] = time.time()
                    self.socket.sendto(package_string , (client_address, client_port))

                print('\nTeste alteração ACK e Sequence Number ********\n') #remove later
                print(json.dumps(object_package.package, sort_keys=True, indent=4))
                print('\n**********************************************') #remove later

                package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
                print ("\nSending a package!\n\n")

                self.toRTT[object_package.package['sequence_number']] = time.time()
                self.socket.sendto(package_string , (client_address, client_port))

                print ('MINHA JANELA')#remove later
                for a in self.window: #remove later
                    print (json.dumps(a, sort_keys=True, indent=4)) #remove later (estranhamente num formatou como no cliente, e preciso formatar em json)
                '''
                    We must coding here functions such as send_data...
                    Start window...timeout... sampleRTT ... to control RWND and CWND...
                    look the sequence logic carefully and talk talk to me if necessary
                '''

    def connection(self, server_address, server_port):
        if str(server_address) == 'localhost':
            server_address = '127.0.0.1'
        object_package = Package()
        self.socket.settimeout(0.1)

        #beginning connection
        object_package.update_values({'destination_port': server_port,'SYN': 1, 'sequence_number': 0})

        package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")
        RTT = time.time()
        self.socket.sendto(package_string , (server_address, server_port))

        if object_package.package['flags']['SYN'] == 1:
            package_string, address = self.socket.recvfrom(self.buffer) #second touch between server and client
            self.sampleRTT = RTT - time.time()
            object_package.package = json.loads(package_string)

            #as the context changed, swaping origin and destination
            object_package.update_values({'origin_port': object_package.package['destination_port'],
                                          'destination_port': object_package.package['origin_port'],
                                          'SYN': 0})

            package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
            print ("\nSending a package!\n\n")
            self.socket.sendto(package_string , (server_address, server_port))

            return (self.socket, (server_address, server_port))
        else:
            print("The server is not prepared to start a connection")

    def close_connection(self, connected):
        self.socket, (address, port) = connected
        object_package = Package()

        object_package.update_values({'FIN': 1})

        package_string = json.dumps(object_package.package, sort_keys=True, indent=4)
        print ("\nSending a package!\n\n")
        self.socket.sendto(package_string, (address, port))

        package_string, (address, port) = self.socket.recvfrom(self.buffer) #second touch between server and client
        object_package.package = json.loads(package_string)

        if object_package.package['flags']['FIN'] == 1:
            print ("\nConnection finished successfully!\n")
        else:
            print ("\nSomething is wrong. The connection was not closed on the server.\n")
        self.socket.close()

    def send_data(self, aData, connected):
        self.socket, (address, port) = connected
        object_package = Package()
        segment = 0
        number_segment = -1
        self.last_ack = None
        self.duploAck = False
        self.triploAck = False

        self.break_in_segments(aData, port)

        #verify if window is empty
        if self.window is None:
            print ('\nThe window is empty. \n')
        else:
            while self.slow_start: #PRECISAMOS IMPLEMENTAR O SLOW START.
                self.verifyRTT((address, port))
                if segment < len(self.window):
                    for i in range(self.cwnd):
                        object_package.package = self.window[segment]

                        self.toRTT[object_package.package['sequence_number']] = time.time()

                        object_package.update_values({'length_header':
                        len(json.dumps(object_package.package, sort_keys=True, indent=4)) -
                        len(object_package.package['data'])})

                        self.window[segment] = json.dumps(object_package.package, sort_keys=True, indent=4)
                        print ("\nSending a package!\n\n")
                        print('tamanho pacote: '+str(len(json.dumps(object_package.package, sort_keys=True, indent=4))))
                        print('tamanho dados: '+str(len(object_package.package['data'])))
                        print (self.window[segment]) #remove later
                        self.socket.sendto(self.window[segment] , (address, port))
                        segment = segment + 1
                else:
                    for i in range(self.cwnd):
                        try:
                            package_string, (address, port) = self.socket.recvfrom(self.buffer)
                        except:
                            if not self.toRTT:
                                break
                            #check RTT timeout
                            continue
                        object_package.package = json.loads(package_string)

                        self.removeRTT(object_package.package['sequence_number'])

                        self.verifyTripleAck(object_package, (address, port))

                        print('\n**********************************************\n') #remove later
                        print('tamanho pacote: '+str(len(package_string)))
                        print('tamanho dados: '+str(len(object_package.package['data'])))
                        print(package_string)
                        print ('MINHA JANELA')#remove later
                        for a in self.window: #remove later
                            print (a) #remove later
                        print('\n**********************************************\n') #remove later

                    self.cwnd = self.cwnd * 2


    def create_package(self, aData, port):
        object_package = Package()

        self.last_seq =  self.getting_sequence_number()

        object_package.update_values({'ACK': 0, 'sequence_number': self.last_seq, 'data': aData, 'destination_port': port })

        self._window(object_package.package)

    def _window(self, package):
        self.window.append(package)

    def break_in_segments(self, aData, port):
        for item in aData:
            temp = item
            while len(temp) > self.MSS:
                variavel = temp[0:self.MSS]
                temp = temp.replace(variavel, "")
                self.create_package(variavel, port) #create segment

            if temp is not None:
                self.create_package(temp, port)

    def verifyTripleAck(self, object_package, address):
        if self.last_ack is None:
            self.last_ack = object_package.package['confirmation_number']
        elif self.last_ack == object_package.package['confirmation_number']:
            if self.duploAck:
                self.triploAck = True

                retrived_package = self.search_package(object_package.package['confirmation_number'])

                ''' Re-send the ackwnoledge package? if cwnd is low? '''
                self.socket.sendto(json.dumps(retrived_package, sort_keys=True, indent=4), address)

            else:
                self.duploAck = True
        else:
            self.last_ack = object_package.package['confirmation_number']
            self.duploAck = False
            self.triploAck = False

    def search_package(self, num_seq):
        for i in self.window:
            j = (json.loads(i))
            if int(num_seq) == j['sequence_number']:
                return j
        print ('Package not found within the window. sequence_number: ' + str(num_seq))
        return 0

    def verifyRTT(self, address):
        if len(self.toRTT) > 0:
            for a in self.toRTT:
                if time.time() - self.toRTT[int(a)] > self.timeout + self.sampleRTT:
                    self.toRTT[a] = time.time()
                    self.socket.sendto(json.dumps(self.search_package(a), sort_keys=True, indent=4), address)

    def removeRTT(self,sequence_number):
        dict = self.toRTT.copy()
        print (self.toRTT)
        for i in self.toRTT:
            if sequence_number >= i:
                dict.pop(i)
        self.toRTT = dict

    def getting_sequence_number(self):
        seq = 0

        if len(self.window) > 0:
            package = self.window[-1]
            seq = package['sequence_number'] + len(package['data'])

        return seq

    def getting_last_ack(self):
        ack = self.window[-1]['confirmation_number']

        if len(self.window) > 1:
            package = self.window[-2]
            ack = package['confirmation_number']

        return ack

    def verify_next_package_sequence(self, last_ack):
        if len(self.window) > 1:
            package = self.window[-1]
            if package['sequence_number'] != last_ack:
                print('Something is wrong... Last ACK is ', last_ack, 'and Sequence Number received was ', package['sequence_number'])
                return False
            else:
                print('OK....')
                return True
        else:
            print('The first ACK received ', last_ack)
            return True
        '''
            Aqui temos que ver se o array de dados vindo do client ultrapassa o MTU...(1500)
            Ultrapassando... deverá ser segmentado os dados... dai que entram os pacotes e a janela...
            a janela é uma lista de pacotes... e aqui se faz importante o numero de sequencia ao segmentar os dados...

            a partir do envio do primeiro pacote devemos começar a calcular o RTT (estimativa de ida e volta)
            no livro é citado o sampleRTT (esse NAO DEVE ser calculado para segmentos retransmitidos.)
            procurar por estimatedRTT (tem uma fórmula específica)


            devemos inserir timeout... entre outros controles
        '''
