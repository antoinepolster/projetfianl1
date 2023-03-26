import socket
import json 

s = socket.socket()

serverAddress = ('0.0.0.0', 8888)
s.connect(serverAddress)

with open('test.json') as json_data:
    identitejoueur = json.load(json_data)
    request = 'identitejoueur'.encode()

print(request)


s.send(request)

s.listen()
response = s.recv() 

with open(response) as json_data:
    if json.load(json_data):
client, addres = s.accept()
message = client.recv(2048).decode()
