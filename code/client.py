import socket
import json

s = socket.socket()

serverAddress = ('localhost', 3000)
s.connect(serverAddress)

with open('joueur.json') as json_data:
    request = json_data.read().encode()
    s.send(request)

