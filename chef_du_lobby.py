#Gère l'ajout de joueurs en donnant des hash qu'elle revele ensuite et en donnant une preuve de travail à faire
"""
//join pour obtenir une preuve de travail à faire
Pour résoudre cette preuve et être accepté : json : id = solve, cle = le_truc_a_travailler, nonce = notre_preuve
"""

import discord
import random
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741

print("Chef du lobby, celui qui permets d'ajouter des joueurs", int(sys.argv[1]))

global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

difficulte = 2**(256)/(10**6)
liste_entrants = []
reputation = random.random()

def hashit(s) :
    return hashlib.sha256(s.encode()).hexdigest()

@client.event
async def on_message(message):
    msg = json.loads(message.content)
    if msg == "//join" :
        _random = random.random()
        nouvelle_reputation = random.random()
        message = '{"string" : '+str(_random)+', "difficulty" : '+str(difficulte)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(nouvelle_reputation) + '}'
        reputation = nouvelle_reputation
        await client.send_message(channel, message)
        liste_entrants.append(_random)
    if msg["id"] == "solve" :
        if msg["cle"] in liste_entrants :
            #On vérifie la preuve de travail
            if hashit(msg["cle"]+msg["nonce"]) <= difficulte :
                #C'est ok
                print("Nouvel arrivant")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)










