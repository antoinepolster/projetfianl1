import socket
import json
from datetime import datetime
import copy
import threading

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

port = 8882

data = {
    "request": "subscribe",
    "port": port,
    "name": "antoinepolster2",
    "matricules": ["200901", "200901"]
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
    return new_board #,print(str(new_board) + '__' + time)

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
    return a, #print(str(a) + '_turn4')

def sendplay(): #reçoit une demande de mouvement et envoie un mouvement prédefini
   state = message['state']
   freetile = state['tile']
   print(str(freetile) + '_freetile')
   board = state['board']
   target = state['target']
   remaining = state['remaining']
   positions = state['positions']

   def try_gates(board): #genere les 48 nouveaux boards (en environ 3/100 de sec)
    time = str(datetime.now())
    liste = [time]
    a = turn4(freetile) 
    for elem in a:
        for gate in GATES:
            b = slideTiles(board, elem, gate)
            liste.append(b)
    with open ('all_boardstest.txt', 'w') as file:
      time2 = str(datetime.now())
      c = str(liste) + time2
      file.write(c)

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
   #print('#__message__start__target__ at__' + time + '#' + '\n' + str(target) + '\n' + '#__message__end__target#' + '\n')
   #print('#__message__start__position__ at__' + time + '#' + '\n' + str(positions) + '\n' + '#__message__end__posistion#' + '\n')
   #print('#__message__start__board__ at__' + time + '#' + '\n' + str(board) + '\n' + '#__message__end__board#' + '\n')

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
             #print('#__message__start#' + '\n' + str(message) + '\n' + '#__message__end#' + '\n')
             if message['request'] == 'ping':
                #print('ping at ####### ' + time + ' #######')
                pong()
             elif ('lives' in message) == True:
                sendplay()
             else :
                pass
        except OSError :
             print('Serveur introuvable, connexion impossible.')