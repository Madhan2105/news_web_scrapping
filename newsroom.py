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
from newsroom1 import scrap

load_dotenv() #loading environment variable
TOKEN = os.getenv('DISCORD_TOKEN') #storing token
GUILD = os.getenv('DISCORD_GUILD')
print(GUILD)

print(TOKEN,GUILD)
client = discord.Client() 

bot = commands.Bot(command_prefix='$')
@tasks.loop(seconds=1200) #run this task every 4 minutes
async def my_background_task():
    channel = client.get_channel(717657784681758720) #connect with the given channel id 
    print(channel)
    if channel is not None:
        my_list = scrap()
        if(my_list):
            for elem in my_list:
                await channel.send(elem)
        # driver = webdriver.Chrome("chromedriver.exe")

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
# driver = webdriver.Chrome("chromedriver.exe")
# driver.maximize_window()
# wait = WebDriverWait(driver, 20)
# eastern = timezone('US/Eastern')
# us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
# print(us_curr_time)
# last_run_time = us_curr_time+ timedelta(minutes=-30)
# driver.get("https://www.accesswire.com/newsroom/")
# main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="w-embed"]')))
# print(main_div) 
# # time.sleep(10)
# article = main_div.find_elements_by_xpath('//div[@class="w-col w-col-9"]')
# print(len(article))
# for a in article:    
#     # print(a)    
#     head = a.find_element_by_xpath('.//div[@class="headlinelink"]')
#     link = head.find_element_by_xpath('.//a')
    
#     date_element  = a.find_element_by_xpath('.//div[@class="date"]')
#     news_date = date_element.text
#     news_date = news_date.replace(" EST","")
#     news_date = datetime.strptime(news_date,'%A, %B %d, %Y %I:%M %p')
#     # print(news_date)
#     if(last_run_time<news_date<us_curr_time):
#         print(link.get_attribute("href"))
# print(us_curr_time)