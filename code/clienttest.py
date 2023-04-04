#################
##    test     ##
#################

import socket
import json
import threading

s = socket.socket()

serverAddress = ('localhost', 3000) #adresse du serveur 
s.connect(serverAddress)

port = 8886

data = {
    "request": "subscribe",
    "port": port,
    "name": "antoinepolster",
    "matricules": ["20090", "20090"]
 }

request = json.dumps(data).encode()
s.send(request)

response = s.recv(2048).decode()
s.close()

serverAddress2 = ('0.0.0.0', port) #mon adresse 

def pong(): #pour rester connecter
   pong = json.dumps({'response': 'pong'}).encode()
   client.send(pong)
   print(message['request'])
   print('ok') 

def play(): #gerer le moove à faire
   with open('moove.json') as json_data:
      client.send(json_data)
   print(message)
   print('message request play')

def state(): #donne l'état du jeu
   print(message)
   print('message state of the game')

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(serverAddress2)
    s.listen()
    s.settimeout(1) # Pour que l'accept() ne bloque que 1 seconde
    while True : 
        try:
          client, serverAddres = s.accept()
          with client:
             message = json.loads(client.recv(2048).decode())
             if message['request'] == 'ping':
                pong()
             elif ( 'live' in message ) == True:
                play()
             elif ( 'players' in message) == True:
                state()
             else :
                pass
        except socket.timeout:
           pass
