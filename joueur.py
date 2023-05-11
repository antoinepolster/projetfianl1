import socket
import json
from gridutils import *
import random

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

port = 4444

name = "Antoine"
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

def pong(): #envoie ping rester connecter
   pong = json.dumps({'response': 'pong'}).encode()
   client.send(pong)


def send_to_serv(elem, gate, position, message): #envoie ce qu'on veut jouer au serveur
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
    print("play")


def sendplay(message): #gére toute la partie mouvement quand on reçoit une request "play"
    state = message['state']
    erros = message['errors']
    target_item = state['target']
    freetile = state['tile']
    board = state['board']
    positions = state['positions']

    target = getTargetPosition(target_item, board)

    display_errors(erros)
    a = wich_player(state, name)

    if a == True:
        old_position_player = positions[0]
    else : 
        old_position_player = positions[1]


    def try_gates(board): #essaie les 48 possibilités pour trouver un chemin
        tilesset = turn4(freetile)
        i = 0 
        for elem in tilesset:
            for gate in GATES:
                b = slideTiles(board, elem, gate)
                i += 1 
                position_player = newPosition(old_position_player, GATES[gate])
                d = path(position_player, target, b)
                if d != None:
                    send_to_serv(elem, gate, new_position(d), "there is a path")
                    return
                
                if (d == None and i == 48):    
                    print('there is no path')
                    r = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
                    send_to_serv(elem, r, newPosition(old_position_player, GATES[r]), "there is no path")
                    return      
    try_gates(board)


with socket.socket() as s: #ouvre un socket, écoute ce qui arrive et l'envoie dans la bonne fonction d'après la valeur de 'request'
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