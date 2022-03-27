import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
#-*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import exceptions  
import csv
from selenium.common.exceptions import NoSuchElementException        
  
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html")
driver.maximize_window()
ActionChains(driver, 20).move_to_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='I Accept']")))).click().perform()



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--headless")

#Création du CSV
csvFile = open("Rating1.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile,delimiter=';', quotechar='"')
csvWriter.writerow(['User','Hotel','Note','Date','Title','Review'])


compteur_reviews=0


for i in range(83):
    #Récupérer tous les hotels de chaque page 
    driver.refresh()
    time.sleep(3)
    elements=driver.find_elements_by_xpath(".//a[contains(@class, 'property_title prominent')]")
    links = []
    Next_Button1=driver.find_element_by_xpath(".//a[contains(@class,'nav next ui_button primary')]").get_attribute("href")
    
    
    for i in range(len(elements)):
        links.append(elements[i].get_attribute('href'))


    for i in range(1,len(links)):
        driver.get(links[i])
        driver.refresh
        
            
        time.sleep(2) # Wait for reviews to load
        
        
        compteur=0
        while(compteur<=10):
            
            reviews = driver.find_elements_by_xpath("//div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")
            compteur+=1
            # Loop through the reviews found
            for i in range(len(reviews)):
                # get the score, date, title and review
                
                score_class = reviews[i].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
                Note = int(score_class.split("_")[3])/10
                Title = reviews[i].find_element_by_xpath(".//a[@class='fCitC']").text
                Review = reviews[i].find_element_by_xpath(".//div[@class='pIRBV _T']").text.replace("\n", "")
                User=reviews[i].find_element_by_xpath(".//a[@class='ui_header_link bPvDb']").text
                Date_Info=reviews[i].find_element_by_xpath(".//span[@class='euPKI _R Me S4 H3']").text
                Date=Date_Info.split(": ")[1]
                try:
                    Hotel = driver.find_element_by_xpath(".//h1[contains(@class, 'fkWsC b d Pn')]").text
                except NoSuchElementException:
                    Hotel=None
                csvWriter.writerow((User,Hotel,Note,Date,Title,Review))  
                compteur_reviews+=1
                
                print(compteur_reviews)
            try:
                Next_Button=driver.find_element_by_xpath(".//a[contains(@class,'ui_button nav next primary ')]")
                Next_Button_click=driver.find_element_by_xpath(".//a[contains(@class,'ui_button nav next primary ')]").get_attribute("href")
                actions = ActionChains(driver)
                actions.move_to_element(Next_Button).perform()
                driver.get(Next_Button_click)
            except NoSuchElementException:
                break 
                 
                
        
        
        
    driver.get(Next_Button1)


# Close CSV file and browser
csvFile.close()
driver.close()
