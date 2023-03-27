import json 

with open('joueur.json') as json_data:
    fichierjoueur = json.load(json_data)

print (fichierjoueur)