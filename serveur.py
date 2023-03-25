import socket
import json 
s = socket.socket()

serverAddress = ('0.0.0.0', 8888)
s.bind(serverAddress)

with open('test.json') as json_data:
    fichierjoueur = json.load(json_data)

s.send(fichierjoueur)
s.listen()

client, addres = s.accept()
message = client.recv(2048).decode()

