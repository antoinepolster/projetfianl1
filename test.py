import json 

with open('test.json') as json_data:
    fichierjoueur = json.load(json_data)

print (fichierjoueur)