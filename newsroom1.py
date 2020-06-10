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

def newsroom_scrap(us_curr_time,last_run_time):
    try:
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        driver.get("https://www.accesswire.com/newsroom/")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="w-embed"]')))
        print(main_div) 
        # time.sleep(10)
        article = main_div.find_elements_by_xpath('//div[@class="w-col w-col-9"]')
        print(len(article))
        my_list = []
        for a in article:    
            # print(a)    
            head = a.find_element_by_xpath('.//div[@class="headlinelink"]')
            # print(head)
            link = head.find_element_by_xpath('.//a')
            
            date_element  = a.find_element_by_xpath('.//div[@class="date"]')
            news_date = date_element.text
            news_date = news_date.replace(" EST","")
            news_date = datetime.strptime(news_date,'%A, %B %d, %Y %I:%M %p')
            keyword = ["nasdaq","nyse","amex"]
            # print(news_date)
            if(last_run_time<news_date<us_curr_time):
                link = str(link.get_attribute("href"))
                link = link.lower()
                print(link)
                if any(x in link for x in keyword):
                    my_list.append(link)
        print("Run Succesfully")
        print(us_curr_time)
        return my_list
    except Exception as e:
        print("Something went Wrong!!,e")
    finally:
        driver.close()    

if( __name__ == "__main__"):
    my_list = newsroom_scrap()
    print(my_list)