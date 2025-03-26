


import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs


web_service=Service(".\\msedgedriver.exe")
drivers=webdriver.Edge(service=web_service)

# 1.parameter = url list
# 2.parameter = drivers
# 3.parameter = file name
def url_list(urls,drivers,file_name):
    i=1
    try:
        with open(file_name,'w',encoding='utf-8') as file:
            # ========================================
          
            for url in urls:
                drivers.get(url)
                wait = WebDriverWait(drivers, 10)
                try:
             
                    ul = wait.until(EC.presence_of_element_located((By.ID,"1")))
                    li_elements=ul.find_elements(By.TAG_NAME,"li")
                    # ========================================
                    for li in li_elements:
                        try:
                            # ========================================
                            # li title
                            a_element=li.find_element(By.TAG_NAME,"a")
                            title_Attribute=a_element.get_attribute("title")
                            titlelist=title_Attribute.split(" ")
                            
                            brand_title=getBrandParameter(url)
                    
                            product_title=" ".join(titlelist[:3])
                            print(f"bulunan title: {title_Attribute}")
                            # ========================================
                            # li price
                            price_element=li.find_element(By.CLASS_NAME, "price-R57b2z0LFOTTCaDIKTgo")
                            price=price_element.text
                            print(f"bulunan price: {price}")
                            # ========================================
                            # li img       
                            noscript_element = li.find_element(By.TAG_NAME, "noscript")
                            noscript_html = noscript_element.get_attribute("innerHTML")
                            soup = BeautifulSoup(noscript_html, "html.parser")
                            img_element = soup.find("img")
                            if img_element:
                                src = img_element["src"]
                                print(f"bulunan image url: {src}")
                            # ======================================== 
                            # productId,productName,productBrandName,productPrice,Description,ımageUrl
                            fullName=str(i)+"|"+ product_title+"|"+brand_title +"|"+price+"|"+title_Attribute+"|"+src
                            i=i+1
                            file.write(fullName + "\n")
                            print(fullName)
                            # ========================================
                        except Exception as inner_e:
                            print(f"li içinde hata: {inner_e}")
                    # ========================================        
                except Exception as outer_e:
                    print(f"sayfada hata:{outer_e}")
            # ========================================        
    except Exception as file_error:
        print(f"Dosyaya yazma hatası: {file_error}")
      
      
# 1.parameter = model list
# 2.parameter = search area
def urls_settings(model_list,area):
    url_list=[]
    for model in model_list:
        string=f"https://www.hepsiburada.com/ara?q={area}&markalar={model}"
        url_list.append(string)
    return url_list

def getBrandParameter(url):
    parsed_url=urlparse(url)
    query_params=parse_qs(parsed_url.query)
    return query_params.get('markalar',[None])[0]

    
# models for area
phone_models=["samsung","xiaomi","apple","huawei","oppo","redmi","honor","poco","vivo"]
computer_models=["asus","lenovo","msi","hp","casper","apple","Acer","dell","monster","huawei"]
tablet_models=["samsung","xiaomi","apple","lenovo","huawei","honor","casper","poco"]
white_goods=["bosch","arcelik","samsung","siemens","beko","profilo","vestel","lg","altus","regal"]
sound_system_models=["apple","samsung","philips","xiaomi","bosch","kiwi"]

# Models
models=[phone_models,computer_models,tablet_models,white_goods,sound_system_models]
models_area=["telefon","laptop","tablet","buzdolabı","ses sistemleri"]
fileName_list=["phone.txt","computer.txt","tablet.txt","fridge.txt","soundsystem.txt"]


def start_program(fileName_list,models,drivers,modelArea):
    i=0
    for model in models:
        url_list(urls_settings(model,modelArea[i]),drivers,fileName_list[i])
        i=i+1
        
        
# Start Program        
start_program(fileName_list,models,drivers,models_area)        
drivers.quit()