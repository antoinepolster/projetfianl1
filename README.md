# Projet final PI2C : Labyrinthe 

## Etudiant 
Polster Antoine 20090

## Bibliothèques utilisées 
### Pour le programme 
__json__ : pour manipuler des fichierq json   
__socket__ : pour pouvoir discuter avec le serveur  
__copy__ : permettre de faire la copie d'un objet   
__math__ : pour certaines opérations mathématiques

### Pour les tests unitaires
__unittest__ : qui est la bibliothèque qui permet de tester ses fonctions

## Gestion globale du programme 
J'ai "séparé" mon programme en 2 : __clienttestpath.py__ et __gridutils.py__ pour pouvoir faire plus facilement mes tests unitaires et pour que ça soit plus facile au niveau méthode de travail

## Gestion de la relation client-serveur
Mon client ouvre un premier scket qu'il utilise pour se connecter au serveur. Une fois que c'est fait il le ferme directement.
Il en ouvre donc un nouveau pour écouter et envoyer des messages sur le port qu'il a spécifié lors de la connexion.

Pour ce qui est de la discussion avec le serveur : mon client reçoit tout les messages qu'importe le contenue et les traites en fonction des clefs du dictionnaire. Chaque message est alors envoyé vers la fonction qui lui correspond.

## Stratégie pour trouver un chemin
* récuperer la freetile et la faire pivoter dans le 4 sens possibles
* pour chaque sens, l'insérer dans le current board et récuper le new board
* essayer de trouver un chemin entre le notre position et la target à l'aide de BFS
    * dés qu'on trouve un chemin : s'arréter 
    * si on ne trouve pas de chemin on essaie en boucle après les 48 essaies on introduit la tile dans une gate random