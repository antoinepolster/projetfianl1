import math

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

def coords2index(i, j):
    return i * 7 + j

def isCoordsValid(i, j):
    return i >= 0 and i < 7 and j >= 0 and j < 7

def index2coords(index):
    return index // 7, index % 7

def newPosition(oldPositionIndex, inputGate):
    if (abs(inputGate['inc']) == 7 and index2coords(inputGate["start"])[1] == index2coords(oldPositionIndex)[1]):
        #print("same col")
        #print(index2coords(oldPositionIndex)[0])
        #print(index2coords(oldPositionIndex)[1])

        if isCoordsValid((index2coords(oldPositionIndex)[0])+int(math.copysign(1, inputGate['inc'])), index2coords(oldPositionIndex)[1]):
            #print('valid', (index2coords(oldPositionIndex)[0]+int(math.copysign(1, inputGate['inc']))))
            return coords2index(index2coords(oldPositionIndex)[0]+int(math.copysign(1, inputGate['inc'])), index2coords(oldPositionIndex)[1])
        else:
            return coords2index((index2coords(oldPositionIndex)[0]+int(math.copysign(1, inputGate['inc']))) % 7, index2coords(oldPositionIndex)[1])

    if (abs(inputGate['inc']) == 1 and index2coords(inputGate["start"])[0] == index2coords(oldPositionIndex)[0]):
        #print("same line")
        #print(index2coords(oldPositionIndex)[0])
        #print(index2coords(oldPositionIndex)[1])
        if isCoordsValid((index2coords(oldPositionIndex)[0]), index2coords(oldPositionIndex)[1]+int(math.copysign(1, inputGate['inc']))):

            #print('coord valid', (index2coords(oldPositionIndex)[0]), index2coords(oldPositionIndex)[1]+int(math.copysign(1, inputGate['inc'])))
            return coords2index(index2coords(oldPositionIndex)[0], (index2coords(oldPositionIndex)[1])+int(math.copysign(1, inputGate['inc'])))
        else:
            return coords2index(index2coords(oldPositionIndex)[0], (index2coords(oldPositionIndex)[1]+int(math.copysign(1, inputGate['inc']))) % 7)
    return oldPositionIndex

print(newPosition(1, GATES["A"]))