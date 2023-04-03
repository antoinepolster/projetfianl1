import socket

address = ('0.0.0.0', 3000)
request = 'hello world'.encode()

with socket.socket() as s:
    s.connect(address)
    s.send(request)
    response = s.recv(2048).decode()

print(response)