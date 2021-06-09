from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import time
import os
import sys
import psutil
import logging

browser = webdriver.Safari()
amountOfRounds = 0


def setupWebdriver():
    browser.get("https://krasenwin.dekamarkt.nl/start")

def fillAllInputs():
    cookieBTN = browser.find_element_by_xpath('/html/body/app-root/app-cookies/div/div/div/div[2]/button')
    cookieBTN.click()

    firstnameInput = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-home/form/div/div[1]/input')
    firstnameInput.send_keys("Amber")
    firstnameInput.send_keys(Keys.TAB)

    lastnameInput = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-home/form/div/div[2]/input')
    lastnameInput.send_keys("Valantine")
    lastnameInput.send_keys(Keys.TAB)

    emailInput = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-home/form/div/div[3]/input')
    emailInput.send_keys("ambervalantine1911@outlook.com")
    emailInput.send_keys(Keys.TAB)

    hitBoxConditions = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-home/form/div/div[5]/label[1]')
    hitBoxConditions.click()

    enterContest = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-home/form/div/div[6]/button')
    enterContest.click()

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    browser.delete_all_cookies()
    browser.close()
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def breakingTheCode():
    codeInput = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-vul-in/form/div/div[1]/input')
    codeInput.clear()
    codeInput.send_keys(randomStringDigits(6))
    codeInput.send_keys(Keys.ENTER)

    amountOfRounds=1

    while(browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-vul-in/form/div/div[2]/p')):
        codeInput = browser.find_element_by_xpath('/html/body/app-root/div/div[1]/div[2]/app-vul-in/form/div/div[1]/input')
        codeInput.clear()

        codeInput.send_keys(randomStringDigits(6))
        codeInput.send_keys(Keys.ENTER)

        amountOfRounds=amountOfRounds+1
        print(amountOfRounds)

        if(amountOfRounds%60==0):
            break

    print("tasks done, now sleeping for 60 seconds")
    time.sleep(58)
    restart_program()            

def main():
    amountOfRounds = 0
    setupWebdriver()
    fillAllInputs()
    browser.implicitly_wait(1)

    breakingTheCode()

if __name__ == "__main__":
    main()

