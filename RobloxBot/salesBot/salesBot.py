# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 21:46:42 2018

@author: Lawrann
"""

import os, time, sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from threading import Thread

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
        
        
def deletePass(driver) : ## take care not to select the dot if it already open, else it will be close and element will not be visible
    buypassdotSelector = '#item-context-menu > a > span'
    confirmSelector = '#confirm-btn'
    deleteSelector = '#delete-item'     
    buypassdotElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(buypassdotSelector))
    buypassdotElement.click()
    deleteElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(deleteSelector))
    deleteElement.click()
    confirmElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(confirmSelector))
    confirmElement.click()

def buyPass(driver):
    buySelector = '#item-details > div.clearfix.price-container > div.action-button > button' 
    confirmSelector = '#confirm-btn' 
    buyElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(buySelector))
    buyElement.click()
    confirmElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(confirmSelector))
    confirmElement.click()
    
    
def begin(username,password):    
    driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe')    
    login(username,password,driver)
    urllist = ('https://web.roblox.com/catalog/3373192709/Tik-Tok-Hoodie',
               'https://web.roblox.com/catalog/3373143176/Tik-Tok-Rose-Red-Crop-Top-w-Skirt',
               'https://www.roblox.com/catalog/3375888847/Rainbow-T-i-k-T-o-k-Outfit'
               )
    while (exit_request==False):
        for url in urllist:
            driver.get(url)
            for i in range(10):
                try:
                    buyPass(driver)
                except:
                    pass
                time.sleep(2.5)
                try:
                    deletePass(driver)
                    time.sleep(2.5)
                    driver.get(url)
                except:
                    continue
                
threads = list()                
exit_request = False
choice = '1'
while(choice == '1'):
    username = input('Enter username:\n')
    password = input('Enter password:\n')
    process = Thread(target=begin, args=[username,password])
    process.start()
    threads.append(process)
    choice = input('Enter 1 to start another account buy and delete')

exit_request = input('Type True to exit')
for i in threads:
    i.join()
sys.exit(0)
    

        
