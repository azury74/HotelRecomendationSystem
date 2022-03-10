#-*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import csv
from selenium.common.exceptions import NoSuchElementException        


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html")



csvFile = open("hotel1.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile,delimiter=';', quotechar='"')
csvWriter.writerow(['Name','Price/night','Rating',"Rank",'Adress',"Phone","Description"])


elements=driver.find_elements_by_xpath(".//a[contains(@class, 'property_title prominent')]")
print(elements)

links = []
for i in range(len(elements)):
    links.append(elements[i].get_attribute('href'))

print(links)

for i in range(len(links)):
    
    driver.get(links[i])
    time.sleep(2) 
    
    info=driver.find_elements_by_xpath(".//div[@class='ui_container is-fluid page-section accessible_red_3']")

    
    Name = info[0].find_element_by_xpath(".//h1[contains(@class, 'fkWsC b d Pn')]").text
   
    score_class = info[0].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
    Rating = score_class.split("_")[3]
    
    try:
        Price= driver.find_element_by_xpath(".//div[contains(@class, 'fzleB b')]").text
    except NoSuchElementException:
        Price= driver.find_element_by_xpath(".//div[contains(@class, 'vyNCd b Wi')]").text
    
    
    
    info_Rank=info[0].find_element_by_xpath(".//div[contains(@class, 'KeVaw')]").text
    Rank=info_Rank.split(" ")[0]
    
    Phone=info[0].find_element_by_xpath(".//span[contains(@class, 'eeFQx ceIOZ yYjkv')]").text
    
    
    Description=driver.find_element_by_xpath(".//div[contains(@class, 'pIRBV _T')]").text
    
       
    Adress=info[0].find_element_by_xpath(".//span[contains(@class, 'ceIOZ yYjkv')]").text
      
    csvWriter.writerow((str(Name),Price,Rating,Rank,str(Adress),str(Phone),str(Description)))
    driver.back()


csvFile.close()
driver.close()
