import socket
import json
from datetime import datetime
from collections import deque
from gridutils import *

#       A     B     C
#    0  1  2  3  4  5  6
# L  7  8  9 10 11 12 13 D
#   14 15 16 17 18 19 20
# K 21 22 23 24 25 26 27 E
#   28 29 30 31 32 33 34
# J 35 36 37 38 39 40 41 F
#   42 43 44 45 46 47 48
#       I     H     G


GATES = {
    "A": {"start": 1, "end": 43, "inc": 7},
    "B": {"start": 3, "end": 45, "inc": 7},
    "C": {"start": 5, "end": 47, "inc": 7},
    "D": {"start": 13, "end": 7, "inc": -1},
    "E": {"start": 27, "end": 21, "inc": -1},
    "F": {"start": 41, "end": 35, "inc": -1},
    "G": {"start": 47, "end": 5, "inc": -7},
    "H": {"start": 45, "end": 3, "inc": -7},
    "I": {"start": 43, "end": 1, "inc": -7},
    "J": {"start": 35, "end": 41, "inc": 1},
    "K": {"start": 21, "end": 27, "inc": 1},
    "L": {"start": 7, "end": 13, "inc": 1},
}

s = socket.socket()

serverAddress = ('localhost', 3000) #adresse du serveur 
s.connect(serverAddress)

port = 8880

name = "test path"
#name = "player_"+str(random.randint(100, 999))
matricule = "20090"

data = {
    "request": "subscribe",
    "port": port,
    "name": name,
    "matricules": [matricule, matricule]
    }

request = json.dumps(data).encode()
s.send(request)

response = s.recv(2048).decode()
s.close()

serverAddress2 = ('0.0.0.0', port) #mon adresse 

def pong(): #pour rester connecter
   pong = json.dumps({'response': 'pong'}).encode()
   client.send(pong)


def send_to_serv(elem, gate, position, message):
    move = { 
        "tile": elem,
        "gate": gate,
        "new_position": position
            }
                
    play = {
        "response": "move",
        "move": move,
        "message": message
            }

    envoie = json.dumps(play).encode()
    client.send(envoie)
    print("play_" + str(play))


def sendplay(message): 
    print("\n" + "_message2_" + str(message))
    state = message['state']
    erros = message['errors']
    target = state['target']
    print(str(target) + "_target1")
    freetile = state['tile']
    board = state['board']
    remainings = state['remaining']
    positions = state['positions']

    display_errors(erros)
    a = wich_player(state, name)

    if a == True:
        old_position_player = positions[0]
        remaining_player = remainings[0]
        position_opponent = positions[1]
    else : 
        old_position_player = positions[1]
        remaining_player = remainings[1]
        position_opponent = positions[0]


    def try_gates(board):
        tilesset = turn4(freetile)
        i = 0 
        for elem in tilesset:
            for gate in GATES:
                b = slideTiles(board, elem, gate)
                i += 1 
                position_player = newPosition(old_position_player, GATES[gate])
                print("position_" + str(position_player))
                d = path(position_player, target, b)
                if d != None:
                    send_to_serv(elem, gate, new_position(d), "there is a path")
                    return
                
                if (d == None and i == 48):    
                    print('there is no path_' + str(i))
                    send_to_serv(elem, "K", newPosition(old_position_player, GATES["K"]), "there is no path")
                    return      
    try_gates(board)


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(serverAddress2)
    s.listen()
    s.settimeout(500)
    while True : 
        try:
          client, serverAddress = s.accept()
          with client:
             message = json.loads(client.recv(16224).decode())
             if message['request'] == 'ping':
                pong()
             elif message['request'] == 'play':
                sendplay(message)
             else :
                print(message)   
        except OSError :
             print('Serveur introuvable, connexion impossible.')