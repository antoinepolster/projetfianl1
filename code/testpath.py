import copy 
from datetime import datetime
from collections import deque

time0 = str(datetime.now())
print(str(time0) + '_start')

board = [
            {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': True, 'S': True, 'W': True, 'item': 0}, 
            {'N': True, 'E': True, 'S': True, 'W': False, 'item': 23}, 
            {'N': False, 'E': True, 'S': True, 'W': True, 'item': 1}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
            {'N': False, 'E': False, 'S': True, 'W': True, 'item': 15}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': True, 'S': True, 'W': False, 'item': 14}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': True, 'S': True, 'W': False, 'item': 2}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': True, 'S': True, 'W': False, 'item': 3}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': False, 'E': True, 'S': True, 'W': True, 'item': 4}, 
            {'N': False, 'E': True, 'S': True, 'W': True, 'item': 23},
            {'N': True, 'E': False, 'S': True, 'W': True, 'item': 5}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': True, 'S': True, 'W': True, 'item': 22}, 
            {'N': False, 'E': True, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': 17}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': True, 'S': True, 'W': False, 'item': 6}, 
            {'N': True, 'E': True, 'S': False, 'W': False, 'item': 16}, 
            {'N': True, 'E': True, 'S': False, 'W': True, 'item': 7}, 
            {'N': True, 'E': False, 'S': True, 'W': True, 'item': 19}, 
            {'N': True, 'E': False, 'S': True, 'W': True, 'item': 8}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': False, 'S': True, 'W': True, 'item': 9}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': True, 'E': True, 'S': True, 'W': False, 'item': 21}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None}, 
            {'N': False, 'E': False, 'S': True, 'W': True, 'item': None}, 
            {'N': True, 'E': True, 'S': False, 'W': True, 'item': 20}, 
            {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
            {'N': False, 'E': True, 'S': True, 'W': False, 'item': None}, 
            {'N': True, 'E': True, 'S': False, 'W': True, 'item': 10}, 
            {'N': True, 'E': True, 'S': False, 'W': False, 'item': None}, 
            {'N': True, 'E': True, 'S': False, 'W': True, 'item': 11}, 
            {'N': True, 'E': False, 'S': True, 'W': False, 'item': None}, 
            {'N': True, 'E': False, 'S': False, 'W': True, 'item': None},
        ]
free = {'N': True, 'E': True, 'S': True, 'W': False, 'item': 23}

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

def slideTiles(board, free, gate): #prend la freetile et l'injecte dans une gate (ici A) on s'en fout de la new_free_tile
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

def turn_tile(tile): #tourne la freetile de 90° vers le gauche mais n'intervient pas sur l'item
    res = copy.deepcopy(tile)
    res["N"] = tile["E"]
    res["E"] = tile["S"]
    res["S"] = tile["W"]
    res["W"] = tile["N"]
    return res

#   a      b
#  d b -> a c
#   c      d

def turn4(tile): #tourne la freetile dans les 4 sens diff
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
        print(res)
        return res
    except IndexError:
        return None

def try_gates(board):
    a = turn4(free)
    i = 0
    for elem in a:
        for gate in GATES:
            b = slideTiles(board, elem, gate)
            i += 1 
            d = path(0, 48, b)
            if d != None:
                print('there is a path')
                print(i)
                return d

def there_is_a_path(board):
    if try_gates(board) != None: 
        print('yes')
        time = str(datetime.now())
        print(time)
    else :
        print('no')
        time1 = str(datetime.now())
        print(str(time1) +'_end')

there_is_a_path(board)