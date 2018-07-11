#Gère l'ajout de joueurs en donnant des hash qu'elle revele ensuite et en donnant une preuve de travail à faire
"""
//join pour obtenir une preuve de travail à faire
Pour résoudre cette preuve et être accepté : json : id = solve, cle = le_truc_a_travailler, nonce = notre_preuve
"""

import discord
import random
import hashlib
import json
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741

print("Chef du lobby, celui qui permets d'ajouter des joueurs")

global client
client = discord.Client()
channel = discord.Object(id=IDSALON)

JOUEURS = 0
difficulte = 2**(256)/(10**6)
liste_entrants = []
reputation = random.random()

def hashit(s) :
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

@client.event
async def on_message(message):
    global reputation
    msg = message.content
    if msg == "//join" :
        _random = random.random()
        nouvelle_reputation = random.random()
        message = '{"id" : "solve_pow", "string" : '+str(_random)+', "difficulty" : '+str(difficulte)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(hasit(str(nouvelle_reputation))) + '}'
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
                _random = random.random()
                nouvelle_reputation = random.random()
                message = '{"id" : "ajout_joueur", "joueurs" : '+str(JOUEURS)+', "reputation_avant" : '+str(reputation)+', "reputation" : '+str(hasit(str(nouvelle_reputation))) + '}'
                reputation = nouvelle_reputation

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(channel, '{"id" : "debut", "reputation" : ' + str(hashit(str(reputation))) + '}')


client.run(TOKEN)
##
def solve(s, difficulte) :
    import random
    s = str(s)
    while True :
        _r = random.random()
        if hashit(s + str(_r)) < difficulte :
            print("Preuve de travail trouvée :", _r)
            #On renvoit le json qui permets de nous intégrer au jeu
            return '{"id" : "solve", "cle" : '+ s + ', "nonce" : '+ str(_r) + '}'








