# le but ici c'est de mettre une tuile pour bloquer l'adversaire entre 4 portes

def random_gate(positions):
	position_opponent = positions[1]
	tilesaround = []
	a = position_opponent - 7
	b = position_opponent + 1
	c = position_opponent + 7
	d = position_opponent - 1
	if a > 0:
		tilesaround.append(a)
	if b < 49:  
		tilesaround.append(b)
	if c < 49:
		tilesaround.append(c)
	if d 
    tilesaround.append(d)
    print(tilesaround)
    
random_gate([0, 48])