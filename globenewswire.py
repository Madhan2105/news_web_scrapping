from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import itertools  
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def scrap_globenewswire(temp_minute):
    try:
        print("temp_minute",temp_minute)
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        eastern = timezone('US/Eastern')
        us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
        us_curr_time = us_curr_time.time()
        minutes = temp_minute
        driver.get("https://www.globenewswire.com/")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="rl-master-container"]')))
        # print(main_div) 
        # time.sleep(10)
        article = driver.find_elements_by_xpath('//div[@class="rl-container"]')
        # print(len(article))
        my_list = []    
        cookies = wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div/a')))
        cookies.click()
        # time.sleep(2)
        wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="main-content-L1"]/div/h1/a')))
        for a in article:   
            # print("1")
            # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')
            # print(head)
            news_date = a.find_element_by_xpath('.//div[@class="meta-margin"]/p/span')
            news_date = news_date.text               
            keyword = ["NASDAQ","NYSE","AMEX"]
            if "minutes" in news_date or "less than a minute ago"==news_date:           
                if "less than a minute ago"==news_date:
                    print("inside less")
                    actions = ActionChains(driver)                
                    link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))        
                    # link = a.find_element_by_xpath('.//h1/a')
                    print(link.text)
                    import time
                    time.sleep(1)
                    actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    head = str(link.text)
                    link = str(link.get_attribute("href"))
                    driver.switch_to.window(driver.window_handles[-1])                                         
                    data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="content-L2"]/span')))
                    data = data.text                
                    driver.close()                
                    driver.switch_to.window(driver.window_handles[0])                                                                                                   
                    if any(x in data for x in keyword):
                        print(head)
                        my_list.append([link,head])                
                        # print(link)
                else:            
                    print("inside else")                                                                                    
                    news_date = news_date[0:2]                             
                    news_date = int(news_date.replace(" ",""))
                    if news_date<=minutes:
                        actions = ActionChains(driver)                
                        link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))        
                        # link = a.find_element_by_xpath('.//h1/a')
                        print(link.text)
                        import time
                        time.sleep(1)
                        actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                        head = str(link.text)
                        link = str(link.get_attribute("href"))
                        driver.switch_to.window(driver.window_handles[-1])                                         
                        data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="content-L2"]/span')))
                        data = data.text                
                        driver.close()                
                        driver.switch_to.window(driver.window_handles[0])                                       
                        if any(x in data for x in keyword):
                            my_list.append([link,head])                        
                            # print(link)
                print(my_list)
        print("Current time",us_curr_time)
        print(my_list)
        print("Run Complete")        
        return my_list
    except Exception as e:
        print("Something went Wrong!!",e)
    finally:
        driver.close()

if( __name__ == "__main__"):    
    my_list = scrap_globenewswire(4)
    print(my_list)    