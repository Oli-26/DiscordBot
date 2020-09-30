# bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
import random


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

version = "0.1"

class Data:
    def __init__(self):
        self.event_active = False
        self.event_name = ""
        self.util_list = []
        
        
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

  
    if message.content == '!version':
        await message.channel.send(version)
        
    if message.content.startswith('!roll', 0, 5):
        try:
            print(message.content[6:])
            roll_time = int(message.content[6:])
            
        except:
            await message.channel.send('Roll Error, invalid input time')
            return
        await message.channel.send('Roll started! Apply with !apply. Roll ends in ' + str(roll_time) + ' seconds')
        bot_data.event_name = "roll"
        bot_data.event_active = True
        util_list = []
        await asyncio.sleep(roll_time)
        bot_data.event_name = ""
        bot_data.event_active = False
        util_list = []
        
        if(len(bot_data.util_list) == 0):
            await message.channel.send('Roll closed due to lack of applicants')
        else:
            await message.channel.send('Roll finished, congratulations ' + random.choice(bot_data.util_list) + '!')
        
        
    if message.content == "!apply" and bot_data.event_active == True and bot_data.event_name == "roll":
        print(message.author.name + ' applied to roll.')
        if(not message.author.name in bot_data.util_list):
            bot_data.util_list.append(message.author.name)

            
bot_data = Data()
client.run(TOKEN)

