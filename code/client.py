import socket
import json 

s = socket.socket()

serverAddress = ('0.0.0.0', 3000)
s.connect(serverAddress)

with open('joueur.json') as json_data:
    identitejoueur = json.load(json_data)
    request = identitejoueur.encode()
    print(identitejoueur)


s.send(request)
