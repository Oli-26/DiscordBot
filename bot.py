# bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
import random
from logs import record
from permissions import permission_level, add_user, get_info, change_permission, find_id_by_name
from encryption import encrypt, decrypt
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
    '''
        This function handles all messages sent by users. 
        First, the users permissions are determined.
        Next, the list of commands are run through and matched to the sent message.
    '''
    
    # We want to ignore messages sent by the bot itself.
    if message.author == client.user:
        return
    
    # Here the permissions of the user are determined. -1 indicates the user does not exist.    
    level = permission_level(message.author.id)

    #If user does not exist, add them to permissions file
    if(level == -1):
        add_user({'name':message.author.name, 'level':0, 'id':message.author.id})
  
    # Following are all the commands.
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
        await message.channel.send('Raffle started! Apply with !apply. Raffle ends in ' + str(roll_time) + ' seconds')
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
            
    if message.content.startswith('!perm', 0, 5) and level >= 1:
        try:
            l = 0
            search_name = ''
            if(len(message.content) != 5):
                search_name = message.content[6:]
                l = permission_level(find_id_by_name(search_name))
            else:
                search_name = message.author.name
                l = level 
            if l == 2:
                await message.channel.send(search_name + ' is an admin')
            if l == 1:
                await message.channel.send(search_name + ' is a moderator')
            if l == 0:
                await message.channel.send(search_name + ' is a user')
            if l == -1:
                await message.channel.send(search_name + ' does not exist')
        except:
            print("search for permissions failed")
    
    if message.content.startswith('!setPermissions', 0, 15) and level >= 1:
        try:
            search_name = ''
            i = 16
            while(message.content[i] != ' '):
                search_name = search_name + message.content[i] 
                i = i + 1
            perms_arg = int(message.content[i+1:])
            if((perms_arg == 0 or perms_arg == 1 or perms_arg == 2) and level >= perms_arg):
                temp_dict = get_info(find_id_by_name(search_name))
                old_level = temp_dict['level']
                temp_dict['level'] = perms_arg
                change_permission(temp_dict)
                record(search_name + " permission level changed from " + str(old_level) + " to " + str(perms_arg))
            
        except:
            print("Changing permissions failed")
        
                    
bot_data = Data()
client.run(TOKEN)

