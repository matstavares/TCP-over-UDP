from API_TCP_UDP import *

object_client = API_TCP_UDP()

#server_IP = raw_input("Insert the server IP: ")

'''while True:
    try:
        server_port = input("Insert the server port: ")
        break
    except:
        print ("You must to inform a integer number!\n")'''

connection = object_client.connection('localhost', 12000)

object_client.send_data({'dados do pacote....'}, connection)

#object_client.close_connection(connection)
