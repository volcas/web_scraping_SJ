# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:27:15 2020

@author: nnair
"""

# WEB SCRAPING 101

# Header files
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd    
from selenium.webdriver.support.select import Select


driver = webdriver.Chrome()

# Function for searching job on Glassdoor
def search_cuisine(cuisine_name):
    """Entering query terms into search box and running job search"""
    
    search_item = driver.find_element_by_class_name("discover-search")
    search_item.send_keys(cuisine_name)    
    driver.find_element_by_id("search_button").click()
    driver.find_element_by_class_name("close").click()
    driver.find_element_by_id("search_button").click()

    return    



main_url = "https://www.zomato.com"
driver.implicitly_wait(5)
driver.maximize_window()

driver.get(main_url)

cuisine_name="Chinese"

print("Searching for " + cuisine_name)


search_cuisine(cuisine_name)
WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//*[@class='result-title hover_feedback zred bold ln24   fontsize0 ']"))

listings = driver.find_elements_by_xpath("//*[@class='result-title hover_feedback zred bold ln24   fontsize0 ']")

print(len(listings))


df = pd.DataFrame(columns=['Name','cuisine','rating','location','url'])

current_window = driver.current_window_handle

for listing in listings: 
    
    url=listing.get_attribute('href')                          
    driver.execute_script('window.open(arguments[0]);', url)
    new_window=driver.window_handles[1]
    driver.switch_to.window(new_window)
    
  
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-7kepeu-0 sc-ivVeuv kBFhIT']"))
    rest_name=driver.find_element_by_xpath("//*[@class='sc-7kepeu-0 sc-ivVeuv kBFhIT']").text
    
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-hdPSEv kBGNIy']"))
    rest_cuisine=driver.find_element_by_xpath("//*[@class='sc-hdPSEv kBGNIy']").text
    
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-cgHJcJ jzevHZ']"))
    rest_rating=driver.find_element_by_xpath("//*[@class='sc-cgHJcJ jzevHZ']").text[0]
    
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-cmIlrE kbEObq']"))
    rest_location=driver.find_element_by_xpath("//*[@class='sc-cmIlrE kbEObq']").text
    
    
    df = df.append({'Name': rest_name,'cuisine': rest_cuisine,'location':rest_location, 'rating':rest_rating,'url':url}, ignore_index=True)   

    driver.close()
    driver.switch_to.window(current_window)
    
            
# df.to_csv("Zomato_data.csv")