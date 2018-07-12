print("Logical clock")

#Faire en sorte que l'horloge passe à l'étape suivante quand tous les joueurs ont confirmés ?
import sys
import discord
import asyncio
import json
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
WAIT = int(sys.argv[1])
debut = False #Regarde quand le jeu est commencé
reputation = None #La réputation du chef de salle

client = discord.Client()
channel = discord.Object(id=IDSALON)
async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    while not client.is_closed:
        #On active l'horloge que si le jeu a commencé
        if debut :
            if counter % 10 != 9 :
                await client.send_message(channel, '{"id" : "clock", "action" : "gossip", "counter" : '+str(counter) + '}')
            else :
                await client.send_message(channel, '{"id" : "clock", "action" : "graphe", "counter" : '+str(counter) + '}')
            print(counter)
            counter += 1
        await asyncio.sleep(WAIT) # task runs every 60 seconds

@client.event
async def on_message(message):
    msg = json.loads(message.content)
    #Si c'est le premier message du chef
    if msg["id"] == "debut" :
        global reputation
        reputation = msg["reputation"]
        #On demarre l'horloge
        await client.send_message(channel, "Début du jeu")
        global debut
        debut = True

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run(TOKEN)