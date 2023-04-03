import json 

with open('state.json') as json_data:
    fichierjoueur = json.load(json_data)
    if ('request' in fichierjoueur) == True:
        print('ok')
    else : 
        print('non')

print( 'request' in fichierjoueur)
print(fichierjoueur)
