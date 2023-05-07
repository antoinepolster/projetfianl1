import copy
import math
from collections import deque

name = "test path"

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

def slideTiles(board, free, gate): #crée un nouveau board en fonction de la tile qu'on inserre dans une certaine gate
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
    return a


def add(A, B):
    return tuple(a + b for a, b in zip(A, B))


def index2coords(index):
    return index // 7, index % 7


def isCoordsValid(i, j): #vérifie que la coordonnée est bien dans le plateau de jeu
    return i >= 0 and i < 7 and j >= 0 and j < 7
# attention parler de cette fonction le j etait un i avant modif

def coords2index(i, j):
    return i * 7 + j

def BFS(start, successors, goals): #trouve le chemin le plus court entre mon joueur et la tagret
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


def path(start, end, board): # regarde si il existe un chemin entre mon joueur et la target
    def successors(index):
        res = []
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            coords = add(index2coords(index), dir)
            dirName = DIRECTIONS[dir]["name"]
            opposite = DIRECTIONS[dirName]["opposite"]
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


def new_position(path): # renvoie la nouvelle position de mon joueur après son déplacement
    a = len(path)
    position = path[a - 1]
    return position


def wich_player(state, name): # me dit si je suis le joueur 1 ou 2 
    players = state['players']
    if players[0] == name:
        return True
    else : 
        return False


def display_errors(errors): # si il y'a une erreur, cette fonction l'affiche dans le terminal
    if len(errors) != 0:
        a = errors[0]
        b = a['message']
        print('_/!\_error_start_/!\_' + '\n' +  str(b) + '\n' +'_/!\_error_end_/!\_')


def newPosition(oldPositionIndex, inputGate): #me donne la nouvelle position de mon joueur si celui-ci se trouve sur une tile qui a bougé
    print("oldpos_" + str(oldPositionIndex))
    print("gate_" + str(inputGate))
    if (abs(inputGate['inc']) == 7 and index2coords(inputGate["start"])[1] == index2coords(oldPositionIndex)[1]):
        if isCoordsValid((index2coords(oldPositionIndex)[0])+int(math.copysign(1, inputGate['inc'])), index2coords(oldPositionIndex)[1]):
            return coords2index(index2coords(oldPositionIndex)[0]+int(math.copysign(1, inputGate['inc'])), index2coords(oldPositionIndex)[1])
        else:
            return coords2index((index2coords(oldPositionIndex)[0]+int(math.copysign(1, inputGate['inc']))) % 7, index2coords(oldPositionIndex)[1])
    if (abs(inputGate['inc']) == 1 and index2coords(inputGate["start"])[0] == index2coords(oldPositionIndex)[0]):
        if isCoordsValid((index2coords(oldPositionIndex)[0]), index2coords(oldPositionIndex)[1]+int(math.copysign(1, inputGate['inc']))):
            return coords2index(index2coords(oldPositionIndex)[0], (index2coords(oldPositionIndex)[1])+int(math.copysign(1, inputGate['inc'])))
        else:
            return coords2index(index2coords(oldPositionIndex)[0], (index2coords(oldPositionIndex)[1]+int(math.copysign(1, inputGate['inc']))) % 7)
    return oldPositionIndex

def getTargetPosition(target, board): # trouve la tuile target à partir de son item
    for i in range(49):
        if board[i]['item'] == target:
            return i