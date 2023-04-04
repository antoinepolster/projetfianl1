import json 

with open('state.json') as json_data:
    fichierjoueur = json.load(json_data)
    if ('request' in fichierjoueur) == True:
        print('ok')
    else : 
        print('non')
        freetile = str(fichierjoueur['tile'])
        with open ('freetile.txt', 'w') as file : 
            file.write(freetile)
            
#print( 'request' in fichierjoueur)
