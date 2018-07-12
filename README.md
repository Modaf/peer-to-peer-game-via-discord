# peer-to-peer-game-via-discord
A simple peer to peer game using discord to centralize all connections (easy to debug and build)

### Structure de donnée

Graphe direct acyclique  
Dans les noeuds on place les actions des joueurs  
Les joueurs communiquent sur le channel main du discord en explicitant chacun qui parle à qui  

### Structure JSON utilisées

* Partage du dag
  * "id" : "dag"
  * "expediteur" : l'expéditeur de ce message
  * "destinataire" : le destinataire de ce message
  * "dag" : le dag
  * "temps" : le temps du jeu à cet instant
* Ce qui est envoyé par l'horloge
  * "id" : "clock"
  * "action" : "gossip" pour que des joueurs partagent leur graphe, "graphe" pour que chacun affiche son graphe
  * "counter" : le temps du jeu (c'est elle qui le définit)
* Début du jeu par le chef du lobby
  * "id" : "debut"
  * "reputation" : le hash d'une chaine aléatoire qu'il révèle après
* Demander une preuve de travail au chef du jeu
  * "//join" sans json
* Livraison de la preuve de la travail par le chef du lobby
  *"id" : "solve_pow"
  * "string" : une chaine de base pour la pow
  * "difficulty" : la difficulté de la preuve de travail demandée
  * "reputation_avant" : revelation de son dernier hash
  * "reputation" : nouveau hash
* Une fois la preuve de travail effectuée ce que renvoit le joueur
  * "id" : "solve"
  * "cle" : la variable "string" d'avant
  * "nonce" : ce qu'il faut concaténer à la clé pour donner une difficulté inférieure à celle demandée
* Réponse du chef du lobby à cette pruve de travail
  * "id" : "ajout_joueur"
  * "joueurs" : le nombre de joueurs de la partie
  * "reputation_avant" : revelation de son dernier hash
  * "reputation" : nouveau hash

### Déroulement du jeu

Le chef du lobby débute et poste en postant des hashs qu'il révèle ensuite. Il demande une preuve de travail pour qu'un joueur rejoine la partie  
Ensuite les joueurs jouent normal, pour l'instant au hasard et ils communiquent jamais dans un même temps  

### Sharding

On considère qu'on a une structure de donnée shardée qui résout déjà la double dépense et on s'intéresse juste au fait de shard sa position dans une carte virtuelle  
Il y a un graphe par endroit de la carte, on sait pas encore trop si ces endroits s'entrecoupent  
Le problème c'est de changer de graphe efficacement  
On poste nos changements de graphe sur ce qu'on nomme la chaine, c'est notre monnaie magique scalable shardée  
On suppose qu'on peut y accéder en O(1) sans couilles diverses, comme si c'était sur la chaine btc. On verra plus tard pour l'implémentation sur plasma, bch ou tempo  
On le poste, chacun des deux graphes signent le fait qu'on peut bien passer de l'un à l'autre  
Le truc c'est que ces graphes peuvent être à nous à 100%, il faut donc une preuve qu'on peut donner à n'importe qui et qui assure qu'on peut être sur ce graphe même si on a un peu triché (par exemple si dans le graphe a nous on faisant un truc, finallement on peut rollback, c'est relou mais on règle que ce problème on verra ensuite (ptet si les zones sont pas grandes osef, et de toute façon l'impact économique est minime)  
Cette preuve ça va être les graphes par lesquels on est passé (ils sont tous sur la chaine) et les temps. Chacun peut vérifier après avec notre vitesse de déplacement
Le truc c'est que si on change trop de fois ça prends trop de temps à vérifier  
Donc chaque joueur doit pouvoir faire des compressions qu'il paye lui même  
On autorise par exemple 1mb comme taille limite de la preuve  
Chaque joueur doit donc à tout moment pouvoir donner 1mb de trucs (wtf ?) qui prouve qu'il a le droit d'être la  
Par exemple si il a fait une boucle, il demande à la chaine de vérifier que c'est vrai. Une fois ceci faitsa preuve est beaucoup plus petite  
Faut encore ajuster 2/3 trucs pour la compression mais ça va être l'idée : chaque joueur doit faire sa preuve soi même facile à vérifier et non juste la méthode du "on publie tout et on laisse 5€ à celui qui va trouver que c'est faux". Cette méthode est trop insécurisée car les gros poissons peuvent tricher, et la c'est exactement ce qu'on veut empécher : que ceux qui controllent des graphes entiers ne puissent pas tricher  