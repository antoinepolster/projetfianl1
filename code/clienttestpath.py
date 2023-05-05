import socket
import json
from datetime import datetime
import copy
import threading
from collections import deque

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
name = "test path"
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
   print(pong)


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


def turn4(tile): #tourne la freetile dans les 3 sens diff + ajoute la freetile
    old_b = tile
    a = [tile]
    for i in range(3):
        b = turn_tile(old_b)
        i += 1 
        a.append(b)
        old_b = copy.deepcopy(b)
    print(a)
    return a


#début du l'ajout
def add(A, B):
    return tuple(a + b for a, b in zip(A, B))


def index2coords(index):
    return index // 7, index % 7


DIRECTIONS = {
    "N": {"coords": (-1, 0), "inc": -7, "opposite": "S"},
    "S": {"coords": (1, 0), "inc": 7, "opposite": "N"},
    "W": {"coords": (0, -1), "inc": -1, "opposite": "E"},
    "E": {"coords": (0, 1), "inc": 1, "opposite": "W"},
    (-1, 0): {"name": "N"},
    (1, 0): {"name": "S"},
    (0, -1): {"name": "W"},
    (0, 1): {"name": "E"},
}


def isCoordsValid(i, j):
    return i >= 0 and i < 7 and j >= 0 and i < 7


def coords2index(i, j):
    return i * 7 + j


def BFS(start, successors, goals):
    q = deque()
    parent = {}
    parent[start] = None
    node = start
    while node not in goals:
        for successor in successors(node):
            if successor not in parent:
                parent[successor] = node
                q.append(successor)
        node = q.popleft()

    res = []
    while node is not None:
        res.append(node)
        node = parent[node]

    return list(reversed(res))


def path(start, end, board):
    def successors(index):
        res = []
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            coords = add(index2coords(index), dir)
            dirName = DIRECTIONS[dir]["name"]
            opposite = DIRECTIONS[dirName]["opposite"]
            # breakpoint()
            if isCoordsValid(*coords):
                if board[index][dirName] and board[coords2index(*coords)][opposite]:
                    res.append(coords2index(*coords))
        return res

    try:
        res = BFS(start, successors, [end])
        print(str(res) + '_mon_chemin')
        return res
    except IndexError:
        return None
#fin de l'ajout

#mauvaise tactique
#def no_direct_path(positions, target_both, freetile, board): #essayer de trouver une gate pour que l'adversaire soit bloqué entre 4 murs
    position_opponent = positions[1]
    a = turn4(freetile)
    i = 0
    for elem in a:
        for gate in GATES:
            b = slideTiles(board, elem, gate)
            i += 1 
            d = path(position_opponent, target_both, b)
            if d == None:
                return gate, elem
            else :
                print(str(d) + '_' + str(i) + '_opponent_path')

#voir test.py pour termine ça 
#def random_gate(positions):
    position_opponent = positions[1]
    tilesaround = []
    a = position_opponent - 7
    b = position_opponent + 1
    c = position_opponent + 7
    d = position_opponent - 1
    tilesaround.append(a, b, c ,d)


def new_position(path):
    a = len(path)
    position = path[a - 1]
    return position


def wich_player(state):
    players = state['players']
    if players[0] == name:
        return True
    else : 
        return False


def display_errors(errors):
    if len(errors) != 0:
        a = errors[0]
        b = a['message']
        print('_/!\_error_start_/!\_' + '\n' +  str(b) + '\n' +'_/!\_error_end_/!\_')


def sendplay(): #reçoit une demande de mouvement et envoie un mouvement prédefini
    state = message['state']
    erros = message['errors']
    target = state['target']
    freetile = state['tile']
    board = state['board']
    remainings = state['remaining']
    positions = state['positions']

    display_errors(erros)
    a = wich_player(state)

    if a == True:
        position_player = positions[0]
        remaining_player = remainings[0]
        position_opponent = positions[1]
    else : 
        position_player = positions[1]
        remaining_player = remainings[1]
        position_opponent = positions[0]

    #print(str(position_player) + '_player_position')
    #print(str(remaining_player) + '_remaining_tresors')

    def try_gates(board):
        a = turn4(freetile)
        i = 0 
        for elem in a:
            for gate in GATES:
                b = slideTiles(board, elem, gate)
                i += 1 
                d = path(position_player, target, b)
                if d != None:
                    position = new_position(d)
                    print(str(i) + 'it is i')

                    move = {
                        "tile": elem,
                        "gate": gate,
                        "new_position": position
                        }
                
                    play = {
                        "response": "move",
                        "move": move,
                        "message": "there is a path"
                        }

                    envoie = json.dumps(play).encode()
                    client.send(envoie)
                    print(str(play) + '_the_play')
                    #print(str(position) + '_new_position')

                    return
                else : #plein de soucis à regler quand je n'ai pas de chemin 
                    try_i = str(str(d) + '_' + str(i))
                    if try_i == 'None_48':
                        print('there is no path')
                        for elem_a in a:
                            for gate_a in GATES:
                                c = slideTiles(board, elem_a, gate_a)
                                e = path(position_opponent, target, c)
                                if e == None:

                                    move_a = {
                                        "tile": elem_a,
                                        "gate": gate_a,
                                        "new_position": position_player
                                        }
                                    
                                    play_a = {
                                        "response": "move",
                                        "move": move_a,
                                        "message": "the opponent is blocked"
                                        }
                                    
                                    envoie_a = json.dumps(play_a).encode()
                                    client.send(envoie_a)
                                    time2 = str(datetime.now())
                                    print(play_a)
                                    print(str(time2) + '_time_send_wrong_path')
                
    try_gates(board)


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(serverAddress2)
    s.listen()
    s.settimeout(500)
    while True : 
        try:
          client, serverAddress = s.accept()
          message = 0 
          with client:
             message = json.loads(client.recv(16224).decode())
             print(message)
             if message['request'] == 'ping':
                pong()
             elif message['request'] == 'play':
                #time = str(datetime.now())
                #print(message)
                #print(str(time) + '_time_start')
                sendplay()
             else :
                print(message)   
        except OSError :
             print('Serveur introuvable, connexion impossible.')