# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 17:05:48 2019

@author: Lawrann
"""

signupUrl= 'https://www.roblox.com/'

print(signupUrl)



import os, time, sys, threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread

urllist = (
            'https://web.roblox.com/catalog/3373192709/Tik-Tok-Hoodie',
             'https://web.roblox.com/catalog/3373143176/Tik-Tok-Rose-Red-Crop-Top-w-Skirt',
             'https://www.roblox.com/catalog/3375888847/Rainbow-T-i-k-T-o-k-Outfit',
             'https://www.roblox.com/catalog/3373340514/Gold-Marshmello',
             'https://www.roblox.com/catalog/3373187172/ORIGINAL-Designer-Jeans',
             'https://www.roblox.com/catalog/3375875753/T-i-k-T-o-k-Pants',
             'https://www.roblox.com/catalog/3375871327/T-i-k-T-o-k-Crop-Top',
             'https://www.roblox.com/catalog/3373174828/Gucci-Rosy-Embroided-Pants',
             'https://www.roblox.com/catalog/3373854669/Tik-Tok-Gradient-Pants-w-Yellow-Crop-Top',
             'https://www.roblox.com/catalog/3373862255/Pink-Crop-with-Designer-Jeans',
             'https://www.roblox.com/catalog/3373859265/Marshmello-Tube-W-Ripped-Jeans',
             'https://www.roblox.com/catalog/3373853626/Tik-Tok-Yellow-Crop-Top',
#             'https://www.roblox.com/catalog/3373841658/Clouds-Iridescent-Open-Shoulder-Top',
#             'https://www.roblox.com/catalog/3373843667/Pastel-Rainbow-Open-Shoulder-Top',
#             'https://www.roblox.com/catalog/3373835532/Starry-Night-Open-Shoulder-Top',
#             'https://www.roblox.com/catalog/3373832720/Starry-Night-Crop-w-Designer-Jeans',
#             'https://www.roblox.com/catalog/3373823747/Pants',
#             'https://www.roblox.com/catalog/3373821132/Hoodie',
#             'https://www.roblox.com/catalog/3373813445/Sparkling-Pink-Blue-Marshmello-Pants',
#             'https://www.roblox.com/catalog/3373812269/Sparkling-Pink-Blue-Marshmello',
#             'https://www.roblox.com/catalog/3373807507/Supreme-Yellow-CUT-SHOULDER-HOODIE',
#             'https://www.roblox.com/catalog/3373803570/Pink-Sakura-slit-off-the-shoulder',
#             'https://www.roblox.com/catalog/3373799756/Nike-Bomber-Jacket',
#             'https://www.roblox.com/catalog/3373791546/unnamed',
#             'https://www.roblox.com/catalog/3373788663/Blue-Shorts-Pants-w-Shoes',
#             'https://www.roblox.com/catalog/3373786529/Nike-Red-Fade-Pants',
#             'https://www.roblox.com/catalog/3373783204/GALACTIC-SPACE-ADIDAS-HOOD',
#             'https://www.roblox.com/catalog/3373780719/Supreme-Red-Camo-Hoodie',
#             'https://www.roblox.com/catalog/3373778158/Gold-Fade-Hoodie',
#             'https://www.roblox.com/catalog/3373490091/Gold-Marshmello-Pants'
               )



lock = threading.Lock()

driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe')    

driver.get(signupUrl)
        
bmonthXpath = '//*[@id="MonthDropdown"]'
bdayXpath = '//*[@id="DayDropdown"]'
byearXpath = '//*[@id="YearDropdown"]'
usernameXpath = '//*[@id="signup-username"]'
passwordXpath = '//*[@id="signup-password"]'
genderXpath = '//*[@id="FemaleButton"]/div'
singupXpath = '//*[@id="signup-button"]'
favoriteXpath = '//*[@id="favorite-icon"]'
#settingsXpath = '//*[@id="nav-settings"]'
#logoutXpath = '//*[@id="popover4398"]/div[2]/ul/li[3]/a'
#logoutSelector = '#popover878550 > div.popover-content > ul > li:nth-child(3) > a'

exit_flag = True

while(exit_flag):
    try:
        bmonthElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(bmonthXpath))
        bdayElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(bdayXpath))
        byearElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(byearXpath))
        usernameElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(usernameXpath))
        passwordElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(passwordXpath))
        genderElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(genderXpath))
        signupElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(singupXpath))
        exit_flag = False
    except:
        driver.get(signupUrl)
        exit_flag = True

#valuerange = 100
#for i in range(valuerange):
    
createuser = 'inputuser'
createpass = 'inputpass'
bmonthElement.click()
bmonthElement.send_keys('a')
bdayElement.click()
bdayElement.send_keys('2')
byearElement.click()
byearElement.send_keys('1')
usernameElement.send_keys(createuser)
passwordElement.send_keys(createpass)
genderElement.click()
signupElement.click()

robloxLogoXpath = '//*[@id="home-avatar-thumb"]'
try:
    WebDriverWait(driver,1000).until(lambda driver: driver.find_element_by_xpath(robloxLogoXpath))
except TimeoutException:
    print('signup failed')
    driver.close()
    sys.exit(0)


first = False
for url in urllist:
    exit_flag = True
    while(exit_flag):
        try:
            driver.get(url)
            favoriteElement = WebDriverWait(driver,1000).until(lambda driver: driver.find_element_by_xpath(favoriteXpath))
            favoriteElement.click()
            if first == False:
                first = input('enter anything to continue')
            exit_flag = False
        except:
            exit_flag = True

driver.close()
#exit_flag = True
#
#while(exit_flag):
#    try:
#        settingsElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(settingsXpath))
#        settingsElement.click()
#        time.sleep(1)
#        logoutElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_css_selector(logoutSelector)) 
#        logoutElement.click()
#        exit_flag = False
#    except:
#        exit_flag = False
