import socket

s = socket.socket()

serverAddress = ('0.0.0.0', 8888)
s.bind(serverAddress)

s.listen()

client, addres = s.accept()
message = client.recv(2048).decode()

