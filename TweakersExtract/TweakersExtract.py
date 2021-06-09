from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os  

import string

options = Options()  
options.add_argument("--headless")  
browser = webdriver.Chrome(executable_path="/Users/jobvermeulen/CheatCodes/PythonScripts/TweakersExtract/chromedriver",options=options)
class CLIcolors:
    BLACK = '\033[0;30;'
    WHITE = '\033[0;37;40m'
    RED = '\033[0;31;47m'
    GREEN = '\033[0;32;'
    YELLOW = '\033[0;33;'
    BLUE = '\033[0;34;'
    PURPLE = '\033[0;35;'
    CYAN = '\033[0;36;'
    NORMAL = '\033[0;37;0m'


def loadpage():
    print(CLIcolors.RED + 'Reaching tweakers.net;')
    browser.get("https://tweakers.net")
    print('Tweakers has been reached, getting information now!' + CLIcolors.NORMAL)
    cookieBTN = browser.find_element_by_xpath('//*[@id="cookieAcceptForm"]/span/button')
    cookieBTN.click()

def getNews():
    items = []

    try:
        newslist = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='news']/div[1]/table")))
        print(CLIcolors.WHITE)
        print("Het laatste Tweakers nieuws van vandaag:")

        rows = newslist.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
        for row in rows:
            columnText = row.find_elements(By.CLASS_NAME, "title")[0]
            if(row.find_elements(By.CLASS_NAME, "publicationTime")):
                columnTime = row.find_elements(By.CLASS_NAME, "publicationTime")[0] 
            if(columnText.find_elements(By.TAG_NAME, "a") and (columnText.text != "") ):
                print(columnTime.text + " -§- "+ columnText.text + ";")
    except:
        print("Could't load the newslist from Tweakers!")
    finally:
        browser.close()

def main():
    loadpage()
    getNews()

if __name__ == "__main__":
    main()