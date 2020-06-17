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
import logging


load_dotenv() #loading environment variable
TOKEN = os.getenv('DISCORD_TOKEN') #storing token
GUILD = os.getenv('DISCORD_GUILD')
print(GUILD)

print(TOKEN,GUILD)
client = discord.Client() 
bot = commands.Bot(command_prefix='$')
@tasks.loop(seconds=120) #run this task every 4 minutes
async def my_background_task():
    print(datetime.now())    
    print("Background Task")
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    logging.info(":Running..")
    logger.info(us_curr_time)
    channel = client.get_channel(717657784681758720) #connect with the given channel id 
    print(channel)
    if channel is not None:
        temp_minute = 2
        last_run_time = us_curr_time - timedelta(minutes=temp_minute)
        logger.info("Accesswire Job Started")
        print("Accesswire Job Started",last_run_time,us_curr_time)
        my_list = newsroom_scrap(us_curr_time,last_run_time,logger)
        print(my_list)
        if(my_list):
            logger.info("Accesswire:Message Sent")
            await channel.send(my_list)
        print("Accesswire Job Completed")
        logging.info("Accesswire Job Completed")
    print(datetime.now())    

@tasks.loop(seconds=120) #run this task every 4 minutes
async def my_background_task1():
    print("Backgroud task1 ")
    print(datetime.now())    
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    logging.info(":Running..")
    logger.info(us_curr_time)
    channel = client.get_channel(722415293925949440) #connect with the given channel id 
    print(channel)
    if channel is not None:
        temp_minute = 2
        last_run_time = us_curr_time - timedelta(minutes=temp_minute)
        logger.info("prnnewswire Job Started")
        print("prnnewswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_prnewswire(us_curr_time,last_run_time,logger)        
        if(my_list):
            await channel.send(my_list)
        print("prnnewswire Job completed")            
        logging.info("prnnewswire Job completed")            


@tasks.loop(seconds=120) #run this task every 4 minutes
async def my_background_task2():
    print(datetime.now())    
    print("Background Task")
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    logging.info(":Running..")
    logger.info(us_curr_time)
    channel = client.get_channel(717657784681758720) #connect with the given channel id 
    print(channel)
    if channel is not None:
        temp_minute = 2
        last_run_time = us_curr_time - timedelta(minutes=temp_minute)
        logger.info("Bussieswire Job Started")
        print("Bussieswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_bussinewire(us_curr_time,last_run_time,logger)
        if(my_list):
            await channel.send(my_list)
        print("Bussieswire Job Completed")
        logging.info("Bussieswire Job Completed")
    print(datetime.now())    

@tasks.loop(seconds=120) #run this task every 4 minutes
async def my_background_task3():
    print("Backgroud task1 ")
    print(datetime.now())    
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    logging.info(":Running..")
    logger.info(us_curr_time)
    channel = client.get_channel(722415293925949440) #connect with the given channel id 
    print(channel)
    if channel is not None:
        temp_minute = 2
        last_run_time = us_curr_time - timedelta(minutes=temp_minute)

        logger.info("globenewswire Job Started")
        print("globenewswire Job Started",last_run_time,us_curr_time)
        my_list = scrap_globenewswire(us_curr_time,temp_minute,logger)
        if(my_list):
            await channel.send(my_list)
        print("globenewswire Job Completed")
        logger.info("globenewswire Job Completed")
    print(datetime.now())    


@my_background_task.before_loop
async def before_example():
    await client.wait_until_ready()                


@my_background_task1.before_loop
async def before_example():
    await client.wait_until_ready()                
    
@my_background_task2.before_loop
async def before_example():
    await client.wait_until_ready()                

@my_background_task3.before_loop
async def before_example():
    await client.wait_until_ready()                

@client.event
async def on_ready():
    my_background_task.start()
    my_background_task1.start()
    my_background_task2.start()
    my_background_task3.start()
    for guild in client.guilds:
        print("guild",guild)
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)    
