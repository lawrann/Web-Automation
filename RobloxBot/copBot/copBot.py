# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 22:18:48 2018

@author: Lawrann
"""

import os, requests,re, time, sys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def hatscan(scanurl, robuxMaxInput, itemname):
    loop = True
    count = 0
    while loop:
        count = count + 1
        checkprice = itemPrice()
        print('scanning..' + str(count))
        if (int(checkprice)<=int(robuxMaxInput)):
            print('Buying item for R$' + checkprice +'...')
            buyPass()
            print('Bought item for R$' + checkprice +'...')
            print('Checking inventory for item...')
            time.sleep(2)
            confirm = chkInventory()
            if (itemname == confirm):
                print('Sniped ' + itemname + ' at R$' + checkprice)
                loop = False
                driver.quit()
            else:
                driver.get(scanurl)
        else:        
            driver.get(scanurl)

def chkInventory(): ## remember to use driver.get to return to previous url
    driver.get('https://www.roblox.com/my/avatar')
    inventorySelector = '#recent-items-container > div.items-list > ul > li:nth-child(1) > div > div > div.item-card-caption > a > div'
    inventoryElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(inventorySelector))
    return inventoryElement.text

def itemName():
    itemNameSelector = '#item-container > div.section-content.top-section > div.item-name-container > h2'
    itemNameElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(itemNameSelector))
    return itemNameElement.text

def itemPrice():
    itempriceSelector = '#item-details > div.clearfix.price-container > div.price-container-text > div.price-info > div > span.text-robux-lg'
    itempriceElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(itempriceSelector))
    itemprice = (itempriceElement.text).replace(',','')
    return itemprice

def userRbx():
    robuxSelector = '#nav-robux'
    robuxElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(robuxSelector))
    robuxElement.click()
    robuxbalSelector = '#nav-robux-balance'
    time.sleep(1)
    robuxbalElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(robuxbalSelector))
    robuxbal = robuxbalElement.text
    robuxPattern = re.compile(r'\d?\d?\d?,?\d?\d?\d?,?\d?\d?\d?')
    robuxbal = re.findall(robuxPattern, robuxbal)
    robuxval = robuxbal[0].replace(',','')
    return robuxval

def authenticateUse():
    authenticatorLink = r'https://www.youtube.com/watch?v=UwVjofrOQbs&t='
    response = requests.get(authenticatorLink)
    soup = BeautifulSoup(response.text, 'html.parser')
    authenticatorWebElement = soup.select_one('head > title')
    authenticatorWebPattern = re.compile(r'\d\d\d\d\d\d\d\d\d\d?\d?|Closed|Free')
    authenticatorWeb = re.findall(authenticatorWebPattern,str(authenticatorWebElement))
    authenticate = authenticatorWeb[0]
    if(authenticate == 'Free'):
        return 'Free'
    elif (authenticate == 'Closed'):
        print('Progam is currently unavailable')
        driver.close()
        sys.exit(0)
    else :
        return 'https://www.roblox.com/catalog/' + authenticate

def searchInput():
#    print('Entered go input')
    goSelector = '#main-view > div.search-bars > div.clearfix.ng-scope > div > div > div > div > button.input-addon-btn > span'
    goElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(goSelector))
    goElement.click()
    time.sleep(1)

def login(username, password):
    print('Logging in...')
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
        WebDriverWait(driver,5).until(lambda driver: driver.find_element_by_xpath(robloxLogoXpath))
    except TimeoutException:
        print('Incorrect username or password, please try again')
        driver.close()
        sys.exit(0)


def deletePass() : ## take care not to select the dot if it already open, else it will be close and element will not be visible
#    buypassdotSelector = '.icon-more'
    confirmSelector = '#confirm-btn'
    deleteSelector = '#delete-item'     
    deleteElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(deleteSelector))
    deleteElement.click()
    confirmElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(confirmSelector))
    confirmElement.click()
    print('Deleted pass')

def buyPass():
    buySelector = '#item-details > div.clearfix.price-container > div.action-button > button' 
    confirmSelector = '#confirm-btn' 
    buyElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(buySelector))
    buyElement.click()
    confirmElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(confirmSelector))
    confirmElement.click()
    
def checkPass():
    buypassdotSelector = '.icon-more' 
    deleteSelector = '#delete-item'
    buypassdotElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(buypassdotSelector))
    buypassdotElement.click()
    try: ##check if user owns the item
        print('Checking for program pass')
        WebDriverWait(driver,1).until(lambda driver: driver.find_element_by_css_selector(deleteSelector))
        print('Owns deprecated pass -- deleting previous pass permission')
        return True #if owns item, returns true, else false
    except TimeoutException:
        print("Doesn't own pass -- buying new pass permission")
        return False
        

print("Welcome to Lawrann's collectible cop bot V0.6")
print("\nUSAGE: This program runs on chrome driver")
#options = webdriver.ChromeOptions()
#options.binary_location = (os.getcwd() + '\Chrome SxS\Application\chrome.exe')
#options.add_argument('headless')
#options.add_argument('window-size=1200x600')
#options.add_argument('log-level=3')
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe')
driver.get(r'https://www.roblox.com/newlogin') 
print('Please login to your roblox account')
ui = input('Enter username:\n')
pi = input('Enter password:\n')
login(ui,pi)
robloxLogoXpath = '//*[@id="home-avatar-thumb"]'
WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="home-avatar-thumb"]')))

print('Welcome \n' + ui + '\nR$' + userRbx())

authenticatedUsers = list()
authenticatedUsers.append('gm6')
authenticatedUsers.append('BoxX01')
notdev = True
for i in authenticatedUsers:
    if (ui.lower() == i.lower()):
        notdev = False

if (notdev == True): 
    buypasslink = authenticateUse()
    if (buypasslink != 'Free'):
        driver.get(buypasslink) ## User is directed to buygamepasslink, checked if he owns the shirt. If user owns the shirt, it is deleted->purchased->deleted, else it is purchased->deleted
        if (checkPass() == True) :
            deletePass()
            time.sleep(3)
        itemVal = itemPrice()
        userRobux = userRbx()
        print('We grant access to our program based on a pay-per-use model, everytime you run this program, it will charge you.')
        selection = input('Buy pay-per-use pass for R$' + itemVal +'? \n1: Proceed\n2: Quit\n')
        if (selection == 2):
            print('Quitting program')
            driver.close()
            sys.exit(0)
        else :
            buyPass()
            print('Pay-per-use pass bought')
    else:
        print('Program is currently free to use')
        
choice = input('Please selection program function\n1 - Snipe bot (Input URL for item and max robux you are willing to pay)\n2 - Unreleased cop bot (Input exact name of item and max robux you are willing to pay)\n')
if (choice == '1'):
    scanurl = input('Paste full link of item you are sniping\n') 
    print('Scanning url...')
    driver.get(scanurl)
    itemVal = itemPrice()
    userRobux = userRbx()
    iName = itemName()
    print('Current price of ' + iName +' : R$' + itemVal + '\nCurrent available robux : R$' + userRobux )
    robuxMaxInput = input('Enter your max snipe value\n')
    while (robuxMaxInput>userRobux):
        robuxMaxInput = input('You do not have enough robux, enter a lower value\n')
    hatscan(scanurl,robuxMaxInput,iName)
if (choice == '2'):
    iname = input('Input exactname of item\n')
    value = input('Enter your max cop value\n')
    driver.get('https://www.roblox.com/catalog/?Category=2&Subcategory=2&Direction=2')
    searchSelector = '#main-view > div.search-bars > div.clearfix.ng-scope > div > div > div > input'
    searchElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(searchSelector))
    searchElement.click()
    searchElement.clear()
    time.sleep(0.5)
    searchElement.send_keys(iname)
    time.sleep(0.5)
    searchInput()
    item1Selector = '#results > ul > li:nth-child(1) > a > div.item-card-caption > div.item-card-name-link > div'
    loop = True
    count = 0
    print("Beging scan for '" + iname + "' at R$" + value)
    while (loop == True):
        count = count + 1
        print('Scanning ... ' + str(count))
        try:
            item1Element = WebDriverWait(driver,2).until(lambda driver: driver.find_element_by_css_selector(item1Selector))
            if (item1Element.text != iname):
                searchInput()
            else:
                item1Element.click()
                buyPass(driver,value)
                print('Copped')
                loop = False
        except TimeoutException:
            searchInput()
driver.quit()
sys.exit(0)