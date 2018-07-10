import sys
try :
    print("Client", int(sys.argv[1]), "sur", int(sys.argv[2]), "joueurs")
except :
    pass
import os
import discord
import json
import random
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
PROPORTION_GOSSIP = 0.3

os.chdir("C:/Users/apzoeiruty/Desktop/peer_to_peer_game/")
import fichier1test

me, nb_joueurs = 0, 0
try :
    me = fichier1test.Personne(int(sys.argv[1]))
    nb_joueurs = int(sys.argv[2])
except :
    me = fichier1test.Personne(1)
    nb_joueurs = 2
    


global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

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
    msg = json.loads(message.content)
    #On regarde si c'est l'horloge
    if msg["id"] == "clock" :
        #Mise à jour de l'horloge interne
        me.temps = int(msg["counter"])
        #On regarde l'action qu'on doit effectuer
        #Si on doit partager notre graphe
        if msg["action"] == "gossip" and msg["counter"]%nb_joueurs == me.id :  #TODO : random.random() < PROPORTION_GOSSIP :
            print("Partage de notre dag")
            message = '{"id" : "dag", "expediteur" : '+str(me.id)+',"destinataire" : '+str(random_dest(me.id, nb_joueurs))+', "dag" : '+me.partage()+', "temps" : '+str(me.temps)+'}' #TODO : prendre un nombre au hasard pour jouer avec plus de joueurs
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
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)










