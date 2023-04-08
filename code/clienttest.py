import socket
import json
from datetime import datetime
import threading
import time

s = socket.socket()

serverAddress = ('localhost', 3000) #adresse du serveur 
s.connect(serverAddress)

port = 8882

time = str(datetime.now())

data = {
    "request": "subscribe",
    "port": port,
    "name": "antoinepolster2",
    "matricules": ["200901", "200901"]
 }

request = json.dumps(data).encode()
s.send(request)

response = s.recv(2048).decode()
s.close()

serverAddress2 = ('0.0.0.0', port) #mon adresse 

def pong(): #pour rester connecter
   pong = json.dumps({'response': 'pong'}).encode()
   client.send(pong)

thread = threading.Thread(target=pong, daemon=True)

def play(): #reçoit une demande de mouvement
   state = message['state']

   freetile = str(state['tile'])  
   with open ('freetile2.txt', 'w') as file: 
      file.write(freetile)

   board = str(state['board'])
   with open ('currentboard2.txt', 'w') as file:
      file.write(board)

   target = str(state['target'])
   with open ('target2.txt', 'w') as file:
      file.write(target)

   remaining = str(state['remaining'])
   with open ('remaining2.txt', 'w') as file:
      file.write(remaining)

   positions = str(state['positions'])
   with open ('position2.txt', 'w') as file:
      file.write(positions)

   with open('freetile2.txt') as file:
      tile = file.read()
      moove = {
    "tile": tile,
    "gate": "A",
    "new_position": 45
      }
      envoie = (json.dumps(moove)).encode()
      s.send(envoie)

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(serverAddress2)
    s.listen()
    s.settimeout(500)
    while True : 
        try:
          client, serverAddres = s.accept()
          with client:
             message = json.loads(client.recv(16224).decode())
             print(message)
             if message['request'] == 'ping':
                print('ping ####### ' + time + ' #######')
                pong()
             elif ('lives' in message) == True:
                play()
             else :
                pass
        except socket.timeout:
           pass
