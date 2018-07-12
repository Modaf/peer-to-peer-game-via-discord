#Gère l'ajout de joueurs en donnant des hash qu'elle revele ensuite et en donnant une preuve de travail à faire
"""
//join pour obtenir une preuve de travail à faire
Pour résoudre cette preuve et être accepté : json : id = solve, cle = le_truc_a_travailler, nonce = notre_preuve
"""
print("Chef du lobby, celui qui permets d'ajouter des joueurs")

#Petite pause pour laisser aux joueurs le temps de join
import time
time.sleep(25)

import discord
import random
import hashlib
import json
import sys
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741


global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

JOUEURS = 0
MAX_JOUEURS = int(sys.argv[1])
difficulte = 2**(256)/(10**6)
liste_entrants = []
reputation = random.random()

def hashit(s) :
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

@client.event
async def on_message(message):
    global reputation
    global JOUEURS
    msg = message.content
    if msg[:6] == "//join" :
        _random = random.random()
        nouvelle_reputation = random.random()
        _message = '{"id" : "solve_pow", "destinataire" : '+msg[7:]+', "string" : '+str(_random)+', "difficulte" : '+str(difficulte)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(hashit(str(nouvelle_reputation))) + '}'
        await client.send_message(channel, _message)
        reputation = nouvelle_reputation
        liste_entrants.append(_random)
    #Sinon on regarde si c'est un objet json
    msg = json.loads(message.content)
    if msg["id"] == "solve" :
        if msg["cle"] in liste_entrants :
            #On vérifie la preuve de travail
            if hashit(str(msg["cle"])+str(msg["nonce"])) <= difficulte :
                #C'est ok
                print("Nouvel arrivant")
                #On supprime la cle
                del(liste_entrants[liste_entrants.index(msg["cle"])])
                #On ajoute un joueur
                JOUEURS += 1
                nouvelle_reputation = random.random()
                _message = '{"id" : "ajout_joueur", "joueurs" : '+str(JOUEURS)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(hashit(str(nouvelle_reputation))) + '}'
                await client.send_message(channel, _message)
                reputation = nouvelle_reputation
                if (JOUEURS == MAX_JOUEURS) :
                    nouvelle_reputation = random.random()
                    _message = '{"id" : "debut", "joueurs" : '+str(JOUEURS)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(hashit(str(nouvelle_reputation))) + '}'
                    await client.send_message(channel, _message)
                    reputation = nouvelle_reputation

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(channel, '{"id" : "premier_message_chef", "reputation" : ' + str(hashit(str(reputation))) + '}')


client.run(TOKEN)






