from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

games=[]

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
driver.get("https://store.rockstargames.com/zh-Hant?_gl=1*1dsltb*_ga*NDEzNzI4MDE0LjE3MTU5MzgwMjc.*_ga_PJQ2JYZDQC*MTcxNTkzODAyNy4xLjEuMTcxNTk0MDY1NC4wLjAuMA..")
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/section/div/div[1]/section/div/div")))
gameboxes=driver.find_elements(By.CSS_SELECTOR, "ul.css-1wz6m9m div > div a")
for gamebox in gameboxes:
    game={"NAME":'', "IMG":'', "GENRES":'',  "URL":'', "INTRODUCE":'', "RELEASEDATE":'', "PAY":'', "PLATEFORM":'', "RATING":'', "SYSREQUIRE":''}
    name=gamebox.get_attribute("data-valuetext")
    game["NAME"]=name
    href=gamebox.get_attribute("href")
    game["URL"]=href
    driver2.get(href)
    time.sleep(2)
    print(name)
    print(href)

    try:
        introduces=driver2.find_element(By.CSS_SELECTOR, "section[data-testid='section-遊戲說明'] section").find_elements(By.TAG_NAME, "p")
        for introduce in introduces:
            game["INTRODUCE"]+=introduce.text
        print(game["INTRODUCE"])
        release=driver2.find_elements(By.CSS_SELECTOR, "dd")
        for rel in release:
            if "發行日期" in rel.text:
                game["RELEASEDATE"]=rel.text.split("發行日期")[-1]
                print(game["RELEASEDATE"])
    except NoSuchElementException:
        pass
    
    try:
        req=driver2.find_element(By.CSS_SELECTOR, "section.css-lrymzi")
    except NoSuchElementException:
        try:
            req=driver2.find_element(By.CSS_SELECTOR, "section.css-1fcucl3")
        except NoSuchElementException:
            req=False
    finally:
        if req:      
            reqs=req.text.split('\n')
            n_req=[]
            temp=''
            for req in reqs:
                if temp != req:
                    n_req.append(req)
                temp=req
            # n_req=n_req[1:]
            print(n_req)
        print('\n')
        if game["INTRODUCE"] != '':
            games.append(game)
            
Rstar=pd.DataFrame(games)
Rstar.to_csv("Rstar.csv", index=False)
Rstar.to_excel("Rstar.xlsx", index=False)
