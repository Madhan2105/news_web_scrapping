from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import asyncio
import os
from newsroom1 import newsroom_scrap
from bussineswire import scrap_bussinewire
from prnewswire import scrap_prnewswire
from globenewswire import scrap_globenewswire

load_dotenv() #loading environment variable
TOKEN = os.getenv('DISCORD_TOKEN') #storing token
GUILD = os.getenv('DISCORD_GUILD')
print(GUILD)

print(TOKEN,GUILD)
client = discord.Client() 

bot = commands.Bot(command_prefix='$')
@tasks.loop(seconds=240) #run this task every 4 minutes
async def my_background_task():
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    channel = client.get_channel(717657784681758720) #connect with the given channel id 
    print(channel)
    if channel is not None:
        temp_minute = 4
        last_run_time = us_curr_time - timedelta(minutes=temp_minute)
        print("Accesswire Job Started",last_run_time,us_curr_time)
        my_list = newsroom_scrap(us_curr_time,last_run_time)
        print(my_list)
        if(my_list):
            await channel.send(my_list)
        print("Accesswire Job Completed")

        print("Bussieswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_bussinewire(us_curr_time,last_run_time)
        if(my_list):
            await channel.send(my_list)
        print("Bussieswire Job Completed")

        print("prnnewswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_prnewswire(us_curr_time,last_run_time)            
        if(my_list):
            await channel.send(my_list)
        print("prnnewswire Job completed")            

        print("globenewswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_globenewswire(temp_minute)
        if(my_list):
            await channel.send(my_list)
        print("globenewswire Job Completed")

@my_background_task.before_loop
async def before_example():
    await client.wait_until_ready()                

@client.event
async def on_ready():
    my_background_task.start()
    for guild in client.guilds:
        print("guild",guild)
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
    )
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
@client.event
async def on_message(message):    
    print("message",message)
    if message.content == 'check':
        await message.channel.send("Yes!")

client.run(TOKEN)    
