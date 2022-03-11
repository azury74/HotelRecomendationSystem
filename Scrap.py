#-*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import csv
from selenium.common.exceptions import NoSuchElementException        


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html")


#Création du CSV
csvFile = open("hoteltest.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile,delimiter=';', quotechar='"')

#Nom des collones 
csvWriter.writerow(['Name','Price_night',"Rank",'Adress',"Phone","Description","Mail",'Rating',"Number_Rating","Location_Rating","Cleanliness_Rating","Service_Rating","Value_Rating","Walking_Grade","Near_Restaurants","Near_Attractions"])


elements=driver.find_elements_by_xpath(".//a[contains(@class, 'property_title prominent')]")


links = []
for i in range(len(elements)):
    links.append(elements[i].get_attribute('href'))


for i in range(4):
    
    driver.get(links[i])
    
    time.sleep(2) 
    
    
    #Différente partie de la page:
    header=driver.find_elements_by_xpath(".//div[@class='ui_container is-fluid page-section accessible_red_3']")
    about=driver.find_elements_by_xpath(".//div[@class='ui_columns uXLfx']")
    
    
    
    #Info du Header :
    Name = header[0].find_element_by_xpath(".//h1[contains(@class, 'fkWsC b d Pn')]").text
    score_class = header[0].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
    Rating = score_class.split("_")[3]
    Rating=int(Rating)/10
    
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
   
    Detail_Rating=about[0].find_elements_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]")
    
    for z in range(len(Detail_Rating)): 
        temp=Detail_Rating[z].get_attribute("class")
        Detail_Rating[z]=temp.split("_")[3]
      
    
    if(len(Detail_Rating)==1):
        Location_Rating=None
        Cleanliness_Rating=None
        Value_Rating=None
        Service_Rating=None
    else :
        Location_Rating=float(Detail_Rating[1])/10
        Cleanliness_Rating=float(Detail_Rating[2])/10
        Service_Rating=float(Detail_Rating[3])/10
        Value_Rating=float(Detail_Rating[4])/10
       
    Number_Rating_info=about[0].find_element_by_xpath(".//span[contains(@class, 'btQSs q Wi z Wc')]").text
    Number_Rating=Number_Rating_info.split(" ")[0]
    
    Adress=header[0].find_element_by_xpath(".//span[contains(@class, 'ceIOZ yYjkv')]").text
      
    
    
    
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
    
    
    
    #Ecriture 
    csvWriter.writerow((str(Name),Price,Rank,str(Adress),str(Phone),str(Description),str(Mail),Rating,Number_Rating,Location_Rating,Cleanliness_Rating,Service_Rating,Value_Rating,Walking_Grade,Near_Restaurants,Near_Attractions))
    driver.back()


csvFile.close()
driver.close()
