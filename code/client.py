import socket
import json 

s = socket.socket()

serverAddress = ('0.0.0.0', 3000)
s.connect(serverAddress)

with open('test.json') as json_data:
    identitejoueur = json.load(json_data)
    request = 'identitejoueur'.encode()

s.send(request)

response = s.recv(2048).decode()

print(response)
print(request)
