import socket
import json
<<<<<<< HEAD
import threading
=======
>>>>>>> 88d8cb5f023b69d365eff3b349a84e57765fa95d

s = socket.socket()

serverAddress = ('localhost', 3000) #adresse du serveur 
s.connect(serverAddress)

port = 8885

data = {
    "request": "subscribe",
    "port": port,
    "name": "antoinepolster",
    "matricules": ["20090", "20090"]
 }

<<<<<<< HEAD
#def 
=======
>>>>>>> 88d8cb5f023b69d365eff3b349a84e57765fa95d

request = json.dumps(data).encode()
s.send(request)

response = s.recv(2048).decode()
s.close()

serverAddress2 = ('0.0.0.0', port) #mon adresse 

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(serverAddress2)
    s.listen()
    s.settimeout(1) # Pour que l'accept() ne bloque que 1 seconde
    while True : 
        try:
          client, serverAddres = s.accept()
<<<<<<< HEAD
          #thread.start()
=======
>>>>>>> 88d8cb5f023b69d365eff3b349a84e57765fa95d
          with client:
             message = json.loads(client.recv(2048).decode())
             if message['request'] == 'ping':
                pong = json.dumps({'response': 'pong'}).encode()
                client.send(pong)
<<<<<<< HEAD
                print(message['request'])
                print(pong)
=======
                print('ok')
>>>>>>> 88d8cb5f023b69d365eff3b349a84e57765fa95d
             else :
                pass
        except socket.timeout:
           pass
