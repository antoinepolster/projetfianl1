import socket
import json
from datetime import datetime
import copy

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

port = 8888
name = "client"

data = {
    "request": "subscribe",
    "port": port,
    "name": name,
    "matricules": ["20090", "20090"]
 }

request = json.dumps(data).encode()
s.send(request)

response = s.recv(2048).decode()
s.close()

serverAddress2 = ('0.0.0.0', port) #mon adresse 

def pong(): #pour rester connecter
   pong = json.dumps({'response': 'pong'}).encode()
   client.send(pong)

def slideTiles(board, free, gate): 
    start = GATES[gate]["start"]
    end = GATES[gate]["end"]
    inc = GATES[gate]["inc"]

    new_board = copy.deepcopy(board)
    dest = end
    src = end - inc
    while dest != start:
        new_board[dest] = new_board[src]
        dest = src
        src -= inc
    new_board[start] = free
    return new_board

def turn_tile(tile): #tourne la freetile de 90°
    res = copy.deepcopy(tile)
    res["N"] = tile["E"]
    res["E"] = tile["S"]
    res["S"] = tile["W"]
    res["W"] = tile["N"]
    return res

#   a      b
#  d b -> a c
#   c      d

def turn4(tile): #tourne la freetile dans les 3 sens diff + ajoute la freetile
    old_b = tile
    a = [tile]
    for i in range(3):
        b = turn_tile(old_b)
        i += 1 
        a.append(b)
        old_b = copy.deepcopy(b)
    return a

def wich_player(state):
    players = state['players']
    if players[0] == name:
        return True
    else : 
        return False

def sendplay(): #reçoit une demande de mouvement et envoie un mouvement prédefini
    state = message['state']
    target = state['target']
    freetile = state['tile']
    board = state['board']
    remainings = state['remaining']
    positions = state['positions']
    a = wich_player(state)

    if a == True:
        position_player = positions[0]
        remaining_player = remainings[0]
    else : 
        position_player = positions[1]
        remaining_player = remainings[1]

    print(position_player)
    print(remaining_player)

    def try_gates(board): #genere les 48 nouveaux boards (en environ 3/100 de sec)
        time = str(datetime.now())
        liste = [time]
        a = turn4(freetile) 
        for elem in a:
            for gate in GATES:
                b = slideTiles(board, elem, gate)
                liste.append(b)

    try_gates(board)

    move = {
   "tile": freetile,
   "gate": "H",
   "new_position": 45
      }

    play = {
   "response": "move",
   "move": move,
   "message": "antoine 1"
      }

    envoie = json.dumps(play).encode() 
    client.send(envoie) #pour l'instant il envoie encore un move prédéfini

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
             elif ('lives' in message) == True:
                sendplay()
             else :
                pass
        except OSError :
             print('Serveur introuvable, connexion impossible.')