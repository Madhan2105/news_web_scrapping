from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def scrap_bussinewire(us_curr_time,last_run_time):
    try:
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        driver.get("https://www.businesswire.com/portal/site/home/news/")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//ul[@class="bwNewsList"]')))
        print(main_div) 
        # time.sleep(10)
        article = main_div.find_elements_by_xpath('//div[@itemscope="itemscope"]')
        print(len(article))
        for a in article:    
            # print(a)    
            link = a.find_element_by_xpath('.//a[@class="bwTitleLink"]')
            # print(link.get_attribute("href"))
            # link = head.find_element_by_xpath('.//a')
            
            date_element  = a.find_element_by_xpath('.//time[@itemprop="dateModified"]')
            # print(date_element.text)
            news_date = date_element.text
            # news_date = news_date.replace(" EST","")
            news_date = datetime.strptime(news_date,'%m/%d/%Y - %I:%M %p')
            # print(news_date)
            keyword = ["NASDAQ","NYSE","AMEX","Technavio"]
            my_list = []
            if(last_run_time<news_date<us_curr_time):
                actions = ActionChains(driver)            
                head = link.text
                actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                link = link.get_attribute("href")
                driver.switch_to.window(driver.window_handles[-1])
                data = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="bw-release-story"]')))
                data = data.text
                # print("----------------------------")
                # print("data",data)
                driver.close()                
                driver.switch_to.window(driver.window_handles[0])
                if any(x in data for x in keyword):
                    my_list.append([link,head])
                print(my_list)
                # print(link.get_attribute("href"))
            # break
        # print(my_list)
        return my_list    
    except Exception as e:
        print("Something went Wrong!!",e)
    finally:
        driver.close()    

if( __name__ == "__main__"):    
    eastern = timezone('US/Eastern')
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
    last_run_time = us_curr_time + timedelta(minutes=-10)        
    my_list = scrap_bussinewire(us_curr_time,last_run_time)
    print(my_list)