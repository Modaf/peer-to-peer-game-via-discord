import os
import discord
import json
import random
import sys
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
PROPORTION_GOSSIP = 0.3

os.chdir("C:/Users/apzoeiruty/Desktop/peer_to_peer_game/")
import fichier1test

me = fichier1test.Personne(int(sys.argv[1]))

print("Client", int(sys.argv[1]))

global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

@client.event
async def on_message(message):
    msg = json.loads(message.content)
    #On regarde si c'est l'horloge
    if msg["id"] == "clock" :
        #Mise à jour de l'horloge interne
        me.temps = int(msg["counter"])
        #On regarde l'action qu'on doit effectuer
        #Si on doit partager notre graphe
        if msg["action"] == "gossip" and msg["counter"]%2 == me.id :  #TODO : random.random() < PROPORTION_GOSSIP :
            print("Partage de notre dag")
            message = '{"id" : "dag", "expediteur" : '+str(me.id)+',"destinataire" : '+str(1-me.id)+', "dag" : '+me.partage()+'}' #TODO : prendre un nombre au hasard pour jouer avec plus de joueurs
            await client.send_message(channel, message)
        #Si on doit afficher notre dag
        if msg["action"] == "graphe" :
            me.dag.graphique(True)
    #On regade si un autre joueur veut communiquer avec nous
    if msg["id"] == "dag" and  msg["destinataire"] == me.id :
        print("Mise à jour de notre dag")
        print(me.partage())
        me.sync_dag(msg["dag"])
        #On ajoute un noeuds à notre graphe, on est destinataire
        me.dag.ajout(me.id, msg["expediteur"], [], me.temps)
        print("Mise à jour effectuée")
        print(me.partage())
        print("")
        print("------")
        print("")
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)










