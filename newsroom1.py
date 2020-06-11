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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
            keyword = ["NASDAQ","NYSE","AMEX"]
            # print(news_date)
            if(last_run_time<news_date<us_curr_time):
                # link.click()
                print(head.text)
                actions = ActionChains(driver)            
                actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                head = head.text
                link = str(link.get_attribute("href"))                    
                driver.switch_to.window(driver.window_handles[-1])
                # driver.get(link)                
                data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="Article"]/div[4]')))
                data = data.text
                # print("----------------------------")
                # print("data",data)
                driver.close()                
                driver.switch_to.window(driver.window_handles[0])
                if any(x in data for x in keyword):
                    my_list.append([link,head])
                print(my_list)
                # break
        print("Run Succesfully")
        print(us_curr_time)
        return my_list
    except Exception as e:
        print("Something went Wrong!!",e)
    finally:
        driver.close()    

if( __name__ == "__main__"):
    eastern = timezone('US/Eastern')
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
    last_run_time = us_curr_time - timedelta(minutes=90)    
    my_list = newsroom_scrap(us_curr_time,last_run_time)
    print(my_list)