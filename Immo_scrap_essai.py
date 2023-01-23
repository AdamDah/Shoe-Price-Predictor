import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from proxy_randomizer import RegisteredProviders
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
html = ""

while True :
    try:
        done = False
        rp = RegisteredProviders()
        rp.parse_providers()
        PROXY = str(rp.get_random_proxy()).split(" ")[0]
        print(PROXY)
        options = webdriver.ChromeOptions()
        #options.add_argument('-headless')
        options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument('-no-sandbox')
        options.add_argument('-disable-dev-shm-usage')
        options.add_argument("enable-automation")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        web_link ="https://www.logic-immo.com/vente-immobilier-ile-de-france,1_0/options/groupprptypesids=1,2,6,7,12"
        driver.get(web_link)
        html = driver.page_source
        if ("https://ct.captcha-delivery.com/c.js" not in str(html)) and ("Cette page ne fonctionne pas"not in str(html)) and ("ERR_TIMED_OUT" not in str(html)) and (len(str(html))>=1000):
            time.sleep(3)
            not_acc_cook = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/span")
            not_acc_cook.click()
            done = True
        #driver.find_element(By.ID,"didomi-notice-agree-button").click()
        #driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[1]/div/div/div/div[2]/form/div[2]/input").send_keys("France").send_keys(Keys.RETURN)
        #search = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[1]/div/div/div/div[8]/div/div[2]/label/a")
        #search.click()
        driver.close()
    except:
        try:
            driver.close()
        except:pass
        continue
    else:
        if done == True:
            print(html)
            break

"""while True :
    try:
        rp = RegisteredProviders()
        rp.parse_providers()
        PROXY = str(rp.get_random_proxy()).split(" ")[0]
        print(PROXY)
        service_args = [
            '--proxy='+PROXY,
        ]
        driver = webdriver.PhantomJS(webdriver.PhantomJS("D:\/Stockage/phantomjs-2.1.1-windows/bin/phantomjs.exe"), service_args=service_args)
        web_link ="https://www.seloger.com/"
        driver.get(web_link)
        html = driver.page_source
        driver.close()
    except:
        continue
    else:
        if "projet" in str(html):
            print(html)
            break

"""

"""from fake_useragent import UserAgent
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')"""
"""
driver = webdriver.PhantomJS("D:\/Stockage/phantomjs-2.1.1-windows/bin/phantomjs.exe")
web_link="https://www.leboncoin.fr/_immobilier_/offres/ile_de_france"
driver.get(web_link)
html = driver.page_source
print(html)
"""

"""
import requests
from bs4 import BeautifulSoup
import requests_cache
import pandas as pd
requests_cache.install_cache("bases_scraping", expire_after=10e5)

url = "https://www.leboncoin.fr/_immobilier_/offres/ile_de_france"
response = requests.get(url)
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v1539013915699088733 t4157550440124640339'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
print(soup)
soup.h1.text.replace("\n", "")
div_fille = soup.find(id="listingAds").find(class_="tabsContent")
all_ads = div_fille.find("ul").findAll("li")
list_all_ads = []
for ads in all_ads:
    infos = ads.find(class_="item_infos")
    title = infos.find(class_="item_title").text.strip()
    try:
        price = infos.find(class_="item_price").text.strip()
    except:
        price = None
    list_all_ads.append({"title":title, "price":price})

df_leboncoin = pd.DataFrame(list_all_ads)
df_leboncoin.head()
"""