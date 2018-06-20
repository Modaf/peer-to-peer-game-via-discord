import os
import discord
import json
import random
import sys
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
PROPORTION_GOSSIP = 0.5

os.chdir("C:/Users/apzoeiruty/Desktop/Implémentation serveur de jeu décentralisé/")
import fichier1test

me = fichier1test.Personne(int(sys.argv[1]))

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
        if msg["action"] == "gossip" and random.random() < PROPORTION_GOSSIP :
            print("Partage de notre dag")
            message = '{"id" : "dag", "expediteur" : '+str(me.id)+',"destinataire" : '+str(me.id)+', "dag" : '+me.partage()+'}'
            await client.send_message(channel, message)
    #On regade si un autre joueur veut communiquer avec nous
    if msg["id"] == "dag" and  msg["destinataire"] == me.id :
        print("Mise à jour de notre dag")
        print(me.partage())
        me.sync_dag(msg["dag"])
        #On ajoute un noeuds à notre graphe, on est destinataire
        me.dag.ajout(me.id, msg["destinataire"], [], me.temps)
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










