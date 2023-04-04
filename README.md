# Projet final : Labyrinthe 

## étudiant 

Polster Antoine 20090

## bibliothèques utilisées 

__json__ : pour manipuler des fichierq json   
__socket__ : pour pouvoir discuter avec le serveur  
__opengl__ : parler de ça

## avancées 
### lancer le serveur 

## lancer serveur
si trop d'arguments : mettre " "
* pwd
* ls
* cd projetfinal1/code
* ls
* cd PI2CChampionshipRunner-main
* ls

## gestion de la relation client-serveur
Mon client ouvre un premier scket qu'il utilise pour se connecter au serveur. Une fois que c'est fait il le ferme directement.
Il en ouvre donc un nouveau pour écouter et envoyer des messages sur le port qu'il a spécifié lors de la connexion.

Pour ce qui est de la discussion avec le serveur : mon client reçoit tout les messages qu'importe le contenue et les traites en fonction des clefs du dictionnaire. Chaque message est alors envoyé vers la fonction qui lui correspond.
