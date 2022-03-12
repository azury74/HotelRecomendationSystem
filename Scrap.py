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
csvWriter.writerow(['Name','Price_night',"Rank",'Adress',"Phone","Website","Description","Hotel_Style","Mail",'Rating',"Number_Rating","Location_Rating","Cleanliness_Rating","Service_Rating","Value_Rating","Walking_Grade","Near_Restaurants","Near_Attractions","Language_Spoken","Wifi","Taxi","Breakfast","Baggage_storage","All_day_front_desk","All_day_check_in","Dry_cleaning","Complimentary_Coffee","Snack_bar","Concierge","Newspaper","Laundry_service","Non_smoking_hotel","Ironing_service","Kid_friendly_buffet","Bar_Lounge","Allergy_free_room","Coffee_tea_maker","Blackout_curtains","Air_conditioning","Housekeeping","Flatscreen_TV","Bathrobes","All_day_check_in","Alarm_clock","Complimentary_toiletries","Snack_bar","Soundproof_rooms","Desk","Minibar","Bath_shower","Safe","Bottled_water","Electric_kettle","Hair_dryer","Family_rooms","Non_smoking_rooms","Valet_parking","Pool","Indoor_pool","Sauna","Hot_tub","Fitness_Center","Rooftop_bar","Spa","Massage","Doorperson","Umbrella","Butler_service","Umbrella","Hammam","Meeting_rooms","Banquet_room","Meeting_rooms","Highchairs_available","Pets_Allowed","Car_hire","Restaurant","Extra_long_beds","Air_purifier","Room_service","Private_balcony","Landmark_view","City_view","Suites","Separate_dining_area","Interconnected_rooms_available","Cable_satellite_TV","Refrigerator","Breakfast_in_the_room","Personal_trainer","Currency_exchange","Paid_private_parking_nearby","Walking_tours","Yoga_room","Books_DVD_music","Strollers"])

compteur_hotel=0

for i in range(83):
    driver.refresh()
    elements=driver.find_elements_by_xpath(".//a[contains(@class, 'property_title prominent')]")
    links = []
    for i in range(elements):
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
        
        
        
        
        #Boucle pour assigner les YES/NO
        if "Free High Speed Internet (WiFi)" in Amenities:
            Wifi="Yes"
        else : 
            Wifi="No"

        if "Taxi service" in Amenities:
            Taxi="Yes"
        else : 
            Taxi="No"
        if "Breakfast available" in Amenities:
            Breakfast="Yes"
        else:
            Breakfast="No"
        if "Baggage storage" in Amenities:
            Baggage_storage="Yes"
        else:
            Baggage_storage="No"
        if "24-hour front desk" in Amenities:
            All_day_front_desk="Yes"
        else:
            All_day_front_desk="No"
        if "24-hour check-in" in Amenities:
            All_day_check_in="Yes"
        else:
            All_day_check_in="No"
        if "Dry cleaning" in Amenities:
            Dry_cleaning="Yes"
        else:
            Dry_cleaning="No"
        if "Complimentary Instant Coffee" in Amenities:
            Complimentary_Coffee="Yes"
        else:
            Complimentary_Coffee="No"
        if "Snack bar" in Amenities:
            Snack_bar="Yes"
        else:
            Snack_bar="No"
        if "Concierge" in Amenities:
            Concierge="Yes"
        else:
            Concierge="No"
        if "Newspaper" in Amenities:
            Newspaper="Yes"
        else:
            Newspaper="No"
        if "Laundry service" in Amenities:
            Laundry_service="Yes"
        else:
            Laundry_service="No"
        if "Non-smoking hotel" in Amenities:
            Non_smoking_hotel="Yes"
        else:
            Non_smoking_hotel="No"
        if "Ironing_service" in Amenities:
            Ironing_service="Yes"
        else:
            Ironing_service="No"
        if "Bar / lounge" in Amenities:
            Bar_Lounge="Yes"
        else:
            Bar_Lounge="No"
        if "Kid-friendly buffet" in Amenities:
            Kid_friendly_buffet="Yes"
        else:
            Kid_friendly_buffet="No"
        if "Valet parking" in Amenities:
            Valet_parking="Yes"
        else:
            Valet_parking="No"
        if "Pool" in Amenities:
            Pool="Yes"
        else:
            Pool="No"
        if "Indoor pool" in Amenities:
            Indoor_pool="Yes"
        else:
            Indoor_pool="No"
        if "Sauna" in Amenities:
            Sauna="Yes"
        else:
            Sauna="No"
        if "Hot tub" in Amenities:
            Hot_tub="Yes"
        else:
            Hot_tub="No"
        if "Fitness Center with Gym / Workout Room" in Amenities:
            Fitness_Center="Yes"
        else:
            Fitness_Center="No"
        if "Rooftop bar" in Amenities:
           Rooftop_bar="Yes"
        else:
            Rooftop_bar="No"
        if "Spa" in Amenities:
            Spa="Yes"
        else:
            Spa="No"
        if "Massage" in Amenities:
            Massage="Yes"
        else:
            Massage="No"
        if "Doorperson" in Amenities:
            Doorperson="Yes"
        else:
            Doorperson="No"
        if "Umbrella" in Amenities:
            Umbrella="Yes"
        else:
            Umbrella="No"
        if "Butler service" in Amenities:
            Butler_service="Yes"
        else:
            Butler_service="No"
        if "Umbrella" in Amenities:
            Umbrella="Yes"
        else:
            Umbrella="No"
        if "Hammam" in Amenities:
            Hammam="Yes"
        else:
            Hammam="No"
        if "Meeting rooms" in Amenities:
            Meeting_rooms="Yes"
        else:
            Meeting_rooms="No"
        if "Banquet room" in Amenities:
            Banquet_room="Yes"
        else:
            Banquet_room="No"
        if "Meeting rooms" in Amenities:
            Meeting_rooms="Yes"
        else:
            Meeting_rooms="No"
        if "Highchairs available" in Amenities:
            Highchairs_available="Yes"
        else:
            Highchairs_available="No"
        if "Pets Allowed ( Dog / Pet Friendly )" in Amenities:
            Pets_Allowed="Yes"
        else:
            Pets_Allowed="No"
        if "Car hire" in Amenities:
            Car_hire="Yes"
        else:
            Car_hire="No"
        if "Restaurant" in Amenities:
            Restaurant="Yes"
        else:
            Restaurant="No"
        if "Breakfast in the room" in Amenities:
            Breakfast_in_the_room="Yes"
        else:
            Breakfast_in_the_room="No"
        if "Personal trainer" in Amenities:
            Personal_trainer="Yes"
        else:
            Personal_trainer="No"
        if "Currency exchange" in Amenities:
            Currency_exchange="Yes"
        else:
            Currency_exchange="No"
        if "Paid private parking nearby" in Amenities:
            Paid_private_parking_nearby="Yes"
        else:
            Paid_private_parking_nearby="No"
        if "Walking tours" in Amenities:
            Walking_tours="Yes"
        else:
            Walking_tours="No"
        if "Yoga room" in Amenities:
            Yoga_room="Yes"
        else:
            Yoga_room="No"
        
        if "Books, DVDs, music for children" in Amenities:
            Books_DVD_music="Yes"
        else:
            Books_DVDs_music="No"
        if "Strollers" in Amenities:
            Strollers="Yes"
        else:
            Strollers="No"
         
            
         
            
         
        if "Allergy-free room" in Features:
            Allergy_free_room="Yes"
        else : 
            Allergy_free_room="No"   
        if "Coffee / tea maker" in Features:
            Coffee_tea_maker="Yes"
        else : 
            Coffee_tea_maker="No"  
        if "Blackout curtains" in Features:
            Blackout_curtains="Yes"
        else : 
            Blackout_curtains="No"

        if "Air conditioning" in Features:
            Air_conditioning="Yes"
        else : 
            Air_conditioning="No"
        if "Housekeeping" in Features:
            Housekeeping="Yes"
        else:
            Housekeeping="No"
        if "Flatscreen TV" in Features:
            Flatscreen_TV="Yes"
        else:
            Flatscreen_TV="No"
        if "Bathrobes" in Features:
            Bathrobes="Yes"
        else:
            Bathrobes="No"
        if "Telephone" in Features:
            Telephone="Yes"
        else:
            All_day_check_in="No"
        if "Wake-up service / alarm clock" in Features:
            Alarm_clock="Yes"
        else:
            Alarm_clock="No"
        if "Complimentary toiletries" in Features:
            Complimentary_toiletries="Yes"
        else:
            Complimentary_toiletries="No"
        if "Snack bar" in Features:
            Snack_bar="Yes"
        else:
            Snack_bar="No"
        if "Soundproof rooms" in Features:
            Soundproof_rooms="Yes"
        else:
            Soundproof_rooms="No"
        if "Desk" in Features:
            Desk="Yes"
        else:
            Desk="No"
        if "Minibar" in Features:
            Minibar="Yes"
        else:
            Minibar="No"
        if "Bath / shower" in Features:
            Bath_shower="Yes"
        else:
            Bath_shower="No"
        if "Safe" in Features:
            Safe="Yes"
        else:
            Safe="No"
        if "Bottled water" in Features:
            Bottled_water="Yes"
        else:
            Bottled_water="No"
           
        if "Electric_kettle" in Features:
            Electric_kettle="Yes"
        else:
            Electric_kettle="No"
           
        if "Hair dryer" in Features:
            Hair_dryer="Yes"
        else:
            Hair_dryer="No"
            
        if "Air purifier" in Features:
            Air_purifier="Yes"
        else:
            Air_purifier="No"
            
        if "Extra long beds" in Features:
            Extra_long_beds="Yes"
        else:
            Extra_long_beds="No"
        if "Private balcony" in Features:
            Private_balcony="Yes"
        else:
            Private_balcony="No"
        if "Room service" in Features:
            Room_service="Yes"
        else:
            Room_service="No"
        if "Interconnected rooms available" in Features:
            Interconnected_rooms_available="Yes"
        else:
            Interconnected_rooms_available="No"
        if "Separate dining area" in Features:
            Separate_dining_area="Yes"
        else:
            Separate_dining_area="No"
            
        if "Refrigerator" in Features:
            Refrigerator="Yes"
        else:
            Refrigerator="No"
        
        if "Cable / satellite TV" in Features:
            Cable_satellite_TV="Yes"
        else:
            Cable_satellite_TV="No"
            
            
            
            
            
            
            
            
            
            
          
        if "Non-smoking rooms" in Types:
            Non_smoking_rooms="Yes"
        else:
            Non_smoking_rooms="No"
           
        if "Family rooms" in Types:
            Family_rooms="Yes"
        else:
            Family_rooms="No"
        
        if "Suites" in Types:
            Suites="Yes"
        else:
            Suites="No"
        if "City view" in Types:
            City_view="Yes"
        else:
            City_view="No"
        if "Landmark view" in Types:
            Landmark_view="Yes"
        else:
            Landmark_view="No"
          
        
            
         
        
        
        #Ecriture 
        csvWriter.writerow((str(Name),Price,Rank,str(Adress),str(Phone),str(Website),str(Description),str(Hotel_Style),str(Mail),Rating,Number_Rating,Location_Rating,Cleanliness_Rating,Service_Rating,Value_Rating,Walking_Grade,Near_Restaurants,Near_Attractions,str(Language_Spoken),Wifi,Taxi,Breakfast,Baggage_storage,All_day_front_desk,All_day_check_in,Dry_cleaning,Complimentary_Coffee,Snack_bar,Concierge,Newspaper,Laundry_service,Non_smoking_hotel,Ironing_service,Kid_friendly_buffet,Bar_Lounge,Allergy_free_room,Coffee_tea_maker,Blackout_curtains,Air_conditioning,Housekeeping,Flatscreen_TV,Bathrobes,All_day_check_in,Alarm_clock,Complimentary_toiletries,Snack_bar,Soundproof_rooms,Desk,Minibar,Bath_shower,Safe,Bottled_water,Electric_kettle,Hair_dryer,Family_rooms,Non_smoking_rooms,Valet_parking,Pool,Indoor_pool,Sauna,Hot_tub,Fitness_Center,Rooftop_bar,Spa,Massage,Doorperson,Umbrella,Butler_service,Umbrella,Hammam,Meeting_rooms,Banquet_room,Meeting_rooms,Highchairs_available,Pets_Allowed,Car_hire,Restaurant,Extra_long_beds,Air_purifier,Room_service,Private_balcony,Landmark_view,City_view,Suites,Separate_dining_area,Interconnected_rooms_available,Cable_satellite_TV,Refrigerator,Breakfast_in_the_room,Personal_trainer,Currency_exchange,Paid_private_parking_nearby,Walking_tours,Yoga_room,Books_DVD_music,Strollers))
        driver.back()
    
    
    #Avoir la page suivante
    lien_next=driver.find_element_by_xpath(".//a[contains(@class, 'nav next ui_button primary')]").get_attribute("href")
    driver.get(lien_next)
    
csvFile.close()
driver.close()
