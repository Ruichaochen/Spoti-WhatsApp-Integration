from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fetchsong import getsong
import fetchsong
from time import sleep
from random import randint
import threading
from time import time

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
        exec(i) # Looking back at this in 2026, this is an absolutely terrible idea. (Why allow ACE?)
                # Would 100% dump as json and load the dictionary instead.
print("To edit settings, open the config.json file and change values as needed")
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\chromedriver")
chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--disable-logging");
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--remote-debugging-port=9222')
if headless:
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")
def findElement(element,identifier,name,timeout = 50):
    inp_xpath_search = "//"+element+"[@"+identifier+"='"+name+"']"
    return WebDriverWait(driver,timeout).until(lambda driver : driver.find_element(By.XPATH, inp_xpath_search))
def findElements(element,identifier,name,timeout = 50):
    inp_xpath_search = "//"+element+"[@"+identifier+"='"+name+"']"
    return WebDriverWait(driver,timeout).until(lambda driver : driver.find_elements(By.XPATH, inp_xpath_search))
pfp = findElement("button","aria-label","Profile",50)
sleep(0.5)
pfp.click()

driver.execute_script("window.Store = Object.assign({}, window.require('WAWebCollections')); setStatus = window.Store.StatusUtils = window.require('WAWebContactStatusBridge').setMyStatus") # Export the set status function

ratelimit_length = 0
is_ratelimited = None
start_time = 0
ratelimit_duration = 0
def ratelimit(status):
    if status == 429:
        if is_ratelimited == 200:
            start_time = time()
        else:
            is_ratelimited = 429
    elif status == 200:
        if is_ratelimited == 429:
            ratelimit_duration = time() - start_time
            open(str(time()) + ".txt","w").write(ratelimit_duration)
            is_ratelimited = 200
        else:
            is_ratelimited = 200
        
    
try:
    while True:
        sleep(randint(wait_floor,wait_ceil))
        song = getsong()
        if song == None:
            print("No song")
        else:
            try:
                print(song)
                
                driver.execute_script('x = setStatus("🎧 '+ " ".join(song) + ' 🎧")')
                status = driver.execute_script("""var something = async() => {
    let result = await x;
    return result["status"];
}
return (await something())""")
                print(status)
            except Exception as error:
                print(error)
finally:
    driver.quit()
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
