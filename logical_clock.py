#Working

import sys
import discord
import asyncio
TOKEN = 'NDU4Mjg2Mjk2MTAwNTAzNTUz.DglckA.Kmgp9Jxk5nhotxcDLu9ytZoTR-M'
IDSALON = 458770508616564741
WAIT = int(sys.argv[1])

client = discord.Client()
async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id=IDSALON)
    while not client.is_closed:
        counter += 1
        await client.send_message(channel, '{"id" : "clock", "counter" : '+str(counter) + '}')
        print(counter)
        await asyncio.sleep(WAIT) # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run(TOKEN)