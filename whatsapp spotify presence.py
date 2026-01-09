from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fetchsong import getsong
import fetchsong
import time
import random
import threading
import requests
import atexit
import win32api
commands = {"put" : {"pause": "https://api.spotify.com/v1/me/player/pause","play": "https://api.spotify.com/v1/me/player/play"},"skip":"https://api.spotify.com/v1/me/player/next"}
try:
    open("config.json","r")
    configpresent = True
except Exception as Error:
    configpresent = False
def setup():
    wait_floor = input("Minimum wait time before updating? ")
    while type(wait_floor) != int:
        try:
            wait_floor = int(wait_floor)
        except Exception as error:
            print("Must be a number")
            wait_floor = input("Minimum wait time before updating?")
    wait_ceil = input("Maximum wait time before updating?")
    while type(wait_ceil) != int:
        try:
            wait_ceil = int(wait_ceil)
            if wait_floor > wait_ceil:
                print("Maximum time must be larger than minimum time")
                raise ValueError('Maximum value is lower than minimum.')
        except Exception as error:
            wait_ceil = input("Maximum wait time before updating?")
    headless = input("Headless mode? (True or False)")
    headless = str(headless)
    while headless != True or headless != True:
        if str(headless).lower() == "true":
            headless = True
            break;
        elif str(headless).lower() == "false":
            headless = False
            break;
        else:
            headless = input("Headless mode? (True or False)")
    config = open("config.json","w")
    config.write("wait_floor = {}\nwait_ceil = {}\nheadless = {}".format(wait_floor,wait_ceil,headless))
    config.close()
    return wait_floor, wait_ceil, headless
if configpresent == False:
    wait_floor, wait_ceil, headless = setup()
    print(wait_floor, wait_ceil, headless)
else:
    f = open("config.json","r")
    for i in f.read().splitlines():
        exec(i) 
print("To edit settings, open the config.json file and change values as needed")
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\chromedriver")
chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--disable-logging");
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--remote-debugging-port=9222')
if headless:
    chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")
def findElement(element,identifier,name,timeout = 50):
    inp_xpath_search = "//"+element+"[@"+identifier+"='"+name+"']"
    return WebDriverWait(driver,timeout).until(lambda driver : driver.find_element(By.XPATH, inp_xpath_search))
def findElements(element,identifier,name,timeout = 50):
    inp_xpath_search = "//"+element+"[@"+identifier+"='"+name+"']"
    return WebDriverWait(driver,timeout).until(lambda driver : driver.find_elements(By.XPATH, inp_xpath_search))
pfp = findElement("div","aria-label","profile photo",50)
time.sleep(0.5)
pfp.click()
time.sleep(1)
def sendheadphones(element, amount):
        while True:
            if len(box.find_elements(By.XPATH, "//span[contains(@style,'background-image: url(')]")) == amount:
                try:
                    while True:
                        if len(box.find_elements(By.XPATH, "//span[contains(@style,'background-image: url(')]")) == amount + 1:
                            break
                        else:
                            if driver.execute_script("return arguments[0].childNodes[0].childNodes[0].nodeName == 'BR'",box) == True:
                                element.send_keys(":head")
                                break;
                            else:
                                send = True
                                if ("head" in str(driver.execute_script("return arguments[0].innerHTML",findElement("span","class","selectable-text copyable-text"))).split(":")[-1]):
                                    send = False
                                if send == True:
                                    element.send_keys(":head")
                            element.send_keys("p")
                            for i in range(driver.execute_script("return arguments[0].innerHTML",findElement("span","class","selectable-text copyable-text")).split(":")[-1].count("p")):
                                element.send_keys(Keys.BACKSPACE)
                            element.send_keys("p")
                            
                            findElement("span","data-emoji","🎧",1).click()
                except Exception as error:
                    print(error)
            else:
                break

@atexit.register
def exitfunc():
    findElement("button","title","Click to edit About",50).click()
    box = findElement("div","role","textbox",50)
    box.click()
    box.send_keys(Keys.CONTROL + "a")
    box.send_keys(Keys.DELETE)
    sendheadphones(box,0)
    box.send_keys(" ")
    box.send_keys(song)
    box.send_keys(" ")
    sendheadphones(box,1)
    findElement("button","title","Click to save, ESC to cancel",50).click()
    driver.quit()
    f = open("closing.txt","w")
    f.write("closed")
    f.close()
win32api.SetConsoleCtrlHandler(exitfunc, True)
##def controls():
##    try:
##        oldmessage = None
##        while True:
##            chat = findElement("span","title","Control")                                
##            holder = driver.execute_script("return arguments[0].parentElement.parentElement.parentElement",chat)
##            message = holder.find_element(By.XPATH, ".//"+"span"+"[@"+"dir"+"='"+"ltr"+"']")
##            command = driver.execute_script("return arguments[0].innerHTML",message)
##            if (command[1:] in commands["put"]) and (command[1:]!=oldmessage):
##                oldmessage = command[1:]
##                print(command[1:])
##                print(commands[command[1:]])
##                pause = requests.put(commands["put"][command[1:]],headers={"Authorization" : "Bearer " + token})
##                print(pause.status_code)
##    except Exception as error:
##        print(error)
##
##threading.Thread(target = controls).start()
            
try:
    while True:
        time.sleep(random.randint(wait_floor,wait_ceil))
        song = getsong()
        if song == None:
            print("No song")
        else:
            try:
                print(song)
                findElement("button","title","Click to edit About",50).click()
                box = findElement("div","role","textbox",50)
                box.click()
                box.send_keys(Keys.CONTROL + "a")
                box.send_keys(Keys.DELETE)
                sendheadphones(box,0)
                box.send_keys(" ")
                box.send_keys(song)
                box.send_keys(" ")
                sendheadphones(box,1)
                findElement("button","title","Click to save, ESC to cancel",50).click()
                try:
                    findElement("span","data-icon","x-alt").click()
                except Exception as error:
                    pass
            except Exception as error:
                print(error)

finally:
    exitfunc()
##input_box_search.send_keys(contact)
##time.sleep(2)
##selected_contact = driver.find_element(By.XPATH, "//span[@title='"+contact+"']")
##selected_contact.click()
##inp_xpath = '//div[@class="_8nE1Y copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
##input_box = driver.find_element_by_xpath(inp_xpath)
##time.sleep(2)
##input_box.send_keys(text + Keys.ENTER)
##time.sleep(2)
##driver.quit()
