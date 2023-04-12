import copy

free = {'N': True, 'E': True, 'S': True, 'W': False, 'item': 23}

def turn_tile(tile): #tourne la freetile de 90° vers le gauche mais n'intervient pas sur l'item
    res = copy.deepcopy(tile)
    res["N"] = tile["E"]
    res["E"] = tile["S"]
    res["S"] = tile["W"]
    res["W"] = tile["N"]
    return res

def turn4(tile):
    old_b = tile
    a = [tile]
    for i in range(3):
        b = turn_tile(old_b)
        i += 1 
        a.append(b)
        old_b = copy.deepcopy(b)
    print(a)

turn4(free)