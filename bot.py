# bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
import random
from logs import record
from permissions import is_admin

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
        return
    if message.content.startswith('!roll', 0, 5):
        min = 0
        max = 0
        if len(message.content) == 5:
            min = 0
            max = 100
        else:    
            try:
                i = 6
                min_str = '' 
                while(message.content[i] != ' '):
                    min_str = min_str + message.content[i]
                    i = i + 1
                    
                max_str = message.content[i+1:]
                min = int(min_str)
                max = int(max_str)
            except:
                await message.channel.send('Roll Error, invalid min and max')
                return    
                
        rand = random.randint(min, max)
        await message.channel.send(str(rand))
        record('roll by ' + message.author.name + '. Result = ' + str(rand))
        return
        
            
    if message.content.startswith('!raffle', 0, 7):
        try:
            print(message.content[8:])
            roll_time = int(message.content[8:])
        except:
            await message.channel.send('Raffle Error, invalid input time')
            return
        record("Raffle called with length of " + str(roll_time))
        await message.channel.send('Raffle started! Apply with !apply. Roll ends in ' + str(roll_time) + ' seconds')
        bot_data.event_name = "raffle"
        bot_data.event_active = True
        util_list = []
        await asyncio.sleep(roll_time)
        bot_data.event_name = ""
        bot_data.event_active = False
        util_list = []
        
        if(len(bot_data.util_list) == 0):
            await message.channel.send('Raffle closed due to lack of applicants')
            record("Raffle failed, lack of applicants")
        else:
            choice = random.choice(bot_data.util_list)
            await message.channel.send('Raffle finished, congratulations ' + choice + '!')
            record("Raffle finished: winner = " + choice)
        
        
    if message.content == "!apply" and bot_data.event_active == True and bot_data.event_name == "raffle":
        print(message.author.name + ' applied to raffle.')
        if(not message.author.name in bot_data.util_list):
            bot_data.util_list.append(message.author.name)
    if message.content == "!perm":
        if is_admin(message.author.name):
            await message.channel.send(message.author.name + ' is an admin')
        else:
            await message.channel.send(message.author.name + ' is a user')
            
bot_data = Data()
client.run(TOKEN)

