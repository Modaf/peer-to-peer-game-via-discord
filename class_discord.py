import sys
try :
    print("Client", int(sys.argv[1]), "sur", int(sys.argv[2]), "joueurs")
except :
    pass
import os
import discord
import json
import random
import time
import hashlib
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
PROPORTION_GOSSIP = 0.3

os.chdir("C:/Users/apzoeiruty/Desktop/peer_to_peer_game/")
import fichier1test


me = fichier1test.Personne(0, 0)


#Si la game a commencé
global a_join
a_join = False
#Si on a été accepté par le chef du lobby
global dejadedans
dejadedans = False
recherche = False #Regarde si on est en train de chercher une preuve de travail ou non
global reputation
reputaion = None #La reputation du chef du lobby
global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

def hashit(s) :
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)
def random_dest(indice, nb_joueurs) :
    """Renvoit l'identifiant d'un joueur différent"""
    #TODO : changer la c'est juste +1
    return (indice+1) % nb_joueurs
    res = indice
    while res == indice :
        res = random.randint(0, nb_joueurs-1)
    return res

@client.event
async def on_message(message):
    print("Joueurs :", me.JOUEURS, "Identifiant :", me.id)
    global a_join
    global dejadedans
    if not a_join :
        msg = json.loads(message.content)
        #Si c'est le premier message du chef
        if msg["id"] == "premier_message_chef" :
            reputation = msg["reputation"]
        #Si c'est le début du jeu
        if msg["id"] == "debut" :
            reputation = msg["reputation"]
            #On demarre le jeu
            #Nombre de joueurs
            while (me.JOUEURS < msg["joueurs"]) :
                me.ajoutJoueur()
            a_join = True
        #Si c'est pour chercher une preuve de travail
        if msg["id"] == "solve_pow" and not dejadedans :
            #Mise à jour de notre identifiant : on est le dernier joueur ajouté
            while (me.JOUEURS < msg["joueurs"]) :
                me.ajoutJoueur()
            me.id = msg["joueurs"] #Pas -1 car en fait ça va rajouter plus tard un joueur à JOUEURS vu qu'on y sera
            s = str(msg["string"])
            difficulte = msg["difficulte"]
            #On attends pour pas que tous les joueurs join en même temps
            #Voir si on fait cette partie en Go
            while True :
                _r = random.random()
                if hashit(s + str(_r)) < difficulte :
                    print("Preuve de travail trouvée :", _r)
                    #On renvoit le json qui permets de nous intégrer au jeu
                    await client.send_message(channel, '{"id" : "solve", "cle" : '+ s + ', "nonce" : '+ str(_r) + '}')
                    #On s'arrête la
                    dejadedans = True
                    a_join = True
                    break
    if a_join :
        msg = json.loads(message.content)
        #On regarde si c'est l'horloge
        if msg["id"] == "clock" :
            #Mise à jour de l'horloge interne
            me.temps = int(msg["counter"])
            #On regarde l'action qu'on doit effectuer
            #Si on doit partager notre graphe
            if msg["action"] == "gossip" and msg["counter"]%me.JOUEURS == me.id :  #TODO : random.random() < PROPORTION_GOSSIP :
                print("Partage de notre dag")
                message = '{"id" : "dag", "expediteur" : '+str(me.id)+',"destinataire" : '+str(random_dest(me.id, me.JOUEURS))+', "dag" : '+me.partage()+', "temps" : '+str(me.temps)+'}' #TODO : prendre un nombre au hasard pour jouer avec plus de joueurs
                await client.send_message(channel, message)
            #Si on doit afficher notre dag
            if msg["action"] == "graphe" : #TODO : les graphes marchent pas
                me.dag.graphique(True, True)
                me.dag.graphique(True, False)
                me.dag.graphique(False)
        #On regade si un autre joueur veut communiquer avec nous
        if msg["id"] == "dag" and  msg["destinataire"] == me.id :
            print("Mise à jour de notre dag")
            print(me.partage())
            me.sync_dag(msg["dag"])
            #On ajoute un noeuds à notre graphe, on est destinataire
            me.dag.ajout(msg["expediteur"], me.id, [], msg["temps"])
            print("Mise à jour effectuée")
            print(me.partage())
            print("")
            print("------")
            print("")
            #Affichae du dag
            #me.dag.graphique_propre()
        #On regarde si un joueur s'est ajouté au jeu
        if msg["id"] == "ajout_joueur" :
            print("Ajout d'un joueur")
            me.ajoutJoueur()
            #On vérifie qu'on est au bon nombre de joueurs
            if me.JOUEURS != msg["joueurs"] :
                print("Mauvais nombre de joueurs")
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(channel, "//join")


client.run(TOKEN)










