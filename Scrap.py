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
csvFile = open("hotel1.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile,delimiter=';', quotechar='"')

#Nom des collones 
csvWriter.writerow(['Name','Price_night',"Rank",'Adress',"Phone","Website","Description","Hotel_Style","Mail",'Rating',"Number_Rating","Location_Rating","Cleanliness_Rating","Service_Rating","Value_Rating","Walking_Grade","Near_Restaurants","Near_Attractions","Language_Spoken"])

compteur_hotel=0

for i in range(83):
    driver.refresh()
    elements=driver.find_elements_by_xpath(".//a[contains(@class, 'property_title prominent')]")
    links = []
    for i in range(len(elements)):
        links.append(elements[i].get_attribute('href'))


    for i in range(1,len(links)):
        
        driver.get(links[i])
        
        time.sleep(2) 
        
        
        #Différente partie de la page: 
        try:
            header=driver.find_elements_by_xpath(".//div[@class='ui_container is-fluid page-section accessible_red_3']")
        except NoSuchElementException:
            header=None
        try:
            about=driver.find_elements_by_xpath(".//div[@class='ui_column  ']")
        except NoSuchElementException:
            about=None
        try:
            good_to_know=driver.find_elements_by_xpath(".//div[@class='ui_column is-6 ']")
        except NoSuchElementException:
            good_to_know=None
        
        try:
            buble=driver.find_elements_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]")
        except NoSuchElementException:
            buble=None
        
     
        
        #Info du Header :
        try:
            Name = header[0].find_element_by_xpath(".//h1[contains(@class, 'fkWsC b d Pn')]").text
        except NoSuchElementException:
            Name=None
        
        try:
            score_class = header[0].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            Rating = score_class.split("_")[3]
            Rating=int(Rating)/10
        except NoSuchElementException:
            score_class=None
        
        try:
            Website= driver.find_element_by_xpath(".//a[contains(@class, 'dOGcA Ci Wc _S C dCQWE _S eCdbd GlpQN')]").get_attribute("href")
        except NoSuchElementException:
            Website=None
        
        try:
            Price= driver.find_element_by_xpath(".//div[contains(@class, 'fzleB b')]").text
        except NoSuchElementException:
            Price= driver.find_element_by_xpath(".//div[contains(@class, 'vyNCd b Wi')]").text
        
        try:
            info_Rank=header[0].find_element_by_xpath(".//div[contains(@class, 'KeVaw')]").text
            Rank=info_Rank.split(" ")[0]
        except NoSuchElementException:
            Rank=None

        try:
            Phone=header[0].find_element_by_xpath(".//span[contains(@class, 'eeFQx ceIOZ yYjkv')]").text
        except NoSuchElementException:
            Phone=None          
       
        
       
        
       #Info du About :
        try:
            Description=driver.find_element_by_xpath(".//div[contains(@class, 'duhwe _T bOlcm bWqJN Ci dMbup')]").text
        except NoSuchElementException:
            Description=None
            
        try:
            Mail_info=driver.find_element_by_xpath(".//a[contains(@class, 'bIWzQ fWKZw')]").get_attribute("href")
            Mail=Mail_info.split(":")[1]
        except NoSuchElementException:
            Mail=None
       
      
        try:
            try:
                try:
                    Hotel_Style_info=good_to_know[3].find_elements_by_xpath(".//div[contains(@class, 'drcGn _R MC S4 _a H')]")
                    Hotel_Style=""
                except exceptions.StaleElementReferenceException:
                    Hotel_Style=None
                    Hotel_Style_info=None
            except IndexError:
                Hotel_Style=None
                Hotel_Style_info=None
        except NoSuchElementException:
            Hotel_Style=None
            Hotel_Style_info=None
            
        
        
        if(Hotel_Style_info== None):
            Hotel_Style=None
        else :
            for k in Hotel_Style_info:
                temp=k.text+" "
                Hotel_Style+=temp
               
            if((Hotel_Style=="") or len(Hotel_Style.strip()) == 0):
                Hotel_Style=None
        
        
        
        try:
            try :
                try:
                    Language_Spoken_info=good_to_know[4].find_elements_by_xpath(".//div[contains(@class, 'drcGn _R MC S4 _a H')]")
                    Language_Spoken=""
                except exceptions.StaleElementReferenceException:
                    Language_Spoken=None
                    Language_Spoken_info=None
            except IndexError:
                Language_Spoken=None
                Language_Spoken_info=None
        except NoSuchElementException:
            Language_Spoken=None
            Language_Spoken_info=None
        
        if(Language_Spoken_info== None):
            Language_Spoken=None
        else :
            for k in Language_Spoken_info:
                temp=k.text+" "
                Language_Spoken+=temp
               
            if((Language_Spoken=="") or len(Language_Spoken.strip()) == 0):
                Language_Spoken=None

        
        tmp_Rating=[]
        for z in range(2,6): 
            temp=buble[z].get_attribute("class")
            tmp_Rating.append(temp.split("_")[3])
        
        #print("------------")
        #print(tmp_Rating)
        #print("END")
        
        if(len(tmp_Rating)==1 or len(tmp_Rating)==0 ):
            Location_Rating=None
            Cleanliness_Rating=None
            Value_Rating=None
            Service_Rating=None
        else :
            Location_Rating=int(tmp_Rating[0])/10
            Cleanliness_Rating=int(tmp_Rating[1])/10
            Service_Rating=int(tmp_Rating[2])/10
            Value_Rating=int(tmp_Rating[3])/10
        
        try:
            Number_Rating_info=about[1].find_element_by_xpath(".//span[contains(@class, 'btQSs q Wi z Wc')]").text
            Number_Rating=Number_Rating_info.split(" ")[0]
        except NoSuchElementException:
            Number_Rating_info=None
        
        try:
            Adress=header[0].find_element_by_xpath(".//span[contains(@class, 'ceIOZ yYjkv')]").text
        except NoSuchElementException:
            Adress=None
        

        #Attraction autour de l'hotel:
        try:
            Walking_Grade=driver.find_element_by_xpath(".//span[contains(@class, 'bpwqy dfNPK')]").text
          
        except NoSuchElementException:
            Walking_Grade=None
            
        try:
            Near_Attractions=driver.find_element_by_xpath(".//span[contains(@class, 'bpwqy VyMdE')]").text
          
        except NoSuchElementException:
            Near_Attractions=None
            
        try:
            Near_Restaurants=driver.find_element_by_xpath(".//span[contains(@class, 'bpwqy eKwbS')]").text
          
        except NoSuchElementException:
            Near_Restaurants=None
        
        
        #Détail propriété:
        element=driver.find_element_by_xpath(".//div[contains(@class, 'dPTxH S4 b _S')]")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        ActionChains(driver, 20).move_to_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Show more']")))).click().perform()
        
        
        
        A=driver.find_elements_by_xpath(".//div[contains(@class,'exYMC K I Pf')]")
        Amenities=A[0].find_elements_by_xpath(".//div[contains(@class,'bUmsU f ME H3 _c')]")
        
        for o in range(len(Amenities)):
            Amenities[o]=Amenities[o].text
        
        
        ActionChains(driver, 20).move_to_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Room features']")))).click().perform()
        
        B=driver.find_elements_by_xpath(".//div[contains(@class,'exYMC K I Pf')]")
        Features=B[0].find_elements_by_xpath(".//div[contains(@class,'bUmsU f ME H3 _c')]")
        
        for o in range(len(Features)):
            Features[o]=Features[o].text
        
        
        ActionChains(driver, 20).move_to_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Room types']")))).click().perform()
        C=driver.find_elements_by_xpath(".//div[contains(@class,'exYMC K I Pf')]")
        
        Types=C[0].find_elements_by_xpath(".//div[contains(@class,'bUmsU f ME H3 _c')]")
        
        for o in range(len(Types)):
            Types[o]=Types[o].text

        compteur_hotel+=1        
        print(compteur_hotel)
        #Ecriture 
        csvWriter.writerow((str(Name),Price,Rank,str(Adress),str(Phone),str(Website),str(Description),str(Hotel_Style),str(Mail),Rating,Number_Rating,Location_Rating,Cleanliness_Rating,Service_Rating,Value_Rating,Walking_Grade,Near_Restaurants,Near_Attractions,str(Language_Spoken)))
        driver.back()
    
    
    #Avoir la page suivante
    lien_next=driver.find_element_by_xpath(".//a[contains(@class, 'nav next ui_button primary')]").get_attribute("href")
    driver.get(lien_next)
    
csvFile.close()
driver.close()
