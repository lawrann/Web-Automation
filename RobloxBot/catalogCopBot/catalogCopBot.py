# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 14:41:45 2018

@author: Lawrann
"""

import os, requests,re, time, sys, threading
from threading import Thread
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def login(username, password,driver):
    print('Logging in...')
    driver.get('https://www.roblox.com/newlogin')
    usernameFieldXpath = '//*[@id="login-username"]'
    userFieldElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(usernameFieldXpath))
    passwordFieldXpath = '//*[@id="login-password"]'
    passwordFieldElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(passwordFieldXpath))
    loginbuttonXpath = '//*[@id="login-button"]'
    loginButtonElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(loginbuttonXpath))
    userFieldElement.clear()
    userFieldElement.send_keys(username)
    passwordFieldElement.clear()
    passwordFieldElement.send_keys(password)
    loginButtonElement = driver.find_element_by_xpath(loginbuttonXpath)
    loginButtonElement.click()
    robloxLogoXpath = '//*[@id="home-avatar-thumb"]'
    try:
        WebDriverWait(driver,1000).until(lambda driver: driver.find_element_by_xpath(robloxLogoXpath))
    except TimeoutException:
        print('Incorrect username or password, please try again')
        driver.close()
        sys.exit(0)
        
def getLink(response):
    assetIDPattern = re.compile(r'"AssetId":\d\d\d\d\d\d\d\d?\d?\d?\d?')
    assetId = re.findall(assetIDPattern, response.text)
    IDpattern = re.findall(r'\d\d\d\d\d\d\d\d?\d?\d?\d?',assetId[0])
    #print(assetId[0])
    #print(IDpattern[0])
    return IDpattern[0]

def getPrice(response):
    bestPricePattern = re.compile(r'"BestPrice":"\d?\d?\d",')
    pricetxt = re.findall(bestPricePattern, response.text)
    price = re.findall(r'\d?\d?\d',pricetxt[0])
    return price[0]

def buycheck(driver, value):
    bcSelector = '#modal-dialog > div > div.modal-body > div.modal-top-body > div.modal-message > span.text-robux'
    bcElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(bcSelector))
    bcElement = (bcElement.text).replace(',','')
    if (int(bcElement) <= int(value)):
        return True
    else:
        return False

def buyPass(driver,value):
    buySelector = '#item-details > div.clearfix.price-container > div.action-button > button' 
    confirmSelector = '#confirm-btn' 
    buyElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(buySelector))
    buyElement.click()
    print('enter buy pass')
    if (buycheck(driver,value)):
        confirmElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(confirmSelector))
        confirmElement.click()
        print('enter buy click')
        print('bought')


rcurl = 'https://www.roblox.com/catalog/'
url = 'https://search.roblox.com/catalog/json?Subcategory=0&Category=2&SortType=4&ResultsPerPage=1'
username = input('Enter username\n')
password = input('Enter password\n')
driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe')
login(username,password,driver)
value = input('Enter value\n')
lock = threading.Lock()
exit_request = False
threads = list()
found = list()

def scanSearch(value,driver):
    enter = True
    while (exit_request == False):
        try:
            enter = True
            response = requests.get(url) ##ur which checks lowest price item
            link = getLink(response)
            price = getPrice(response)
        except IndexError:
            print('Index error, too many requests')
            time.sleep(5)
            print('Resuming')
            response = requests.get(url)
            enter = False
        if (enter == True) :
            if(int(value)>=int(price)):
                found.append(price)
                with lock:
                    driver.get(rcurl+link)
                    buyPass(driver,value)
            print('scanned ' + price)
    
for i in range(2):
    print('Opening thread ' + str(i))
    process = Thread(target=scanSearch, args=[value, driver])
    process.start()
    threads.append(process)
    time.sleep(0.5)
    
exit_request = input('type to exit\n')
for i in threads:
    i.join()
for i in range(len(found)):
    print(i)
driver.close()
sys.exit(0)

