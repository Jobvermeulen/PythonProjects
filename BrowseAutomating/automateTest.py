from selenium import webdriver;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser.get('https://www.nu.nl')

btn = browser.find_element_by_xpath('//*[@id="sanoma-consent-accept-button"]')
btn.click()

lijst = browser.find_elements_by_xpath('//*[@id="main"]/div[1]/div[2]/div/div/div')

for element in lijst:
    print('ik was hier!')
    id = element.get_attribute('id')
    elementId = browser.find_element_by_xpath(u'//*[@id=id]/a/div/h1')
    print (elementId.text)

time.sleep(4)
browser.close()
quit()