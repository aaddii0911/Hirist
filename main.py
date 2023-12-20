import requests
from bs4 import BeautifulSoup
import gspread
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
import time
from datetime import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

url = 'https://www.hirist.com/k/reactjs-jobs.html?locName=any%20location&locIds=0&exp=0&ref=homepagetag'

driver = webdriver.Chrome()
driver.get(url)

l= {
    'Date': [],
    'Company': [],
    'Position': [],
    'Location': [],
    'Apply Here': [],
    'Posting Time': [],
    'Seniority Level': []
}
di = {
    "Data Analyst": "https://www.hirist.com/k/reactjs-jobs.html?locName=any%20location&locIds=0&exp=0&ref=homepagetag"
}
for i in range(len(list(di.values()))):
    driver.get(list(di.values())[i])
    time.sleep(3)
    for k in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    f = soup.find_all('div', class_="job-description col-sm-9 col-xl-9")
    for a in range(len(f)):
        try:
            job = f[a]
        except:
            continue
        try:
            c = job.find('div', class_='job-title').text
            company = c.split(' -')[0]
        except:
            company = 'No Info'
        try:
            job_title = job.find('div', class_='job-title').text
        except:
            job_title = 'No Info'
        try:
            req = job.find('div', class_='job-fields').find('span', class_='dark-grey col-year').text
        except:
            req = 'No Info'
        try:
            location = job.find('div', class_='job-fields').find('span', id_='location').find('ul').text
        except:
            location = 'No Info'
        try:
            link = 'https://hirist.com'+job.find('div', class_='job-title').find('a')['href']
        except:
            link = 'No Info'
        try:
            posted_on = job.find('div', class_='job-fields').find('span',class_='original dark-grey').text
        except:
            posted_on = 'No Info'

        l['Date'].append(datetime.today().strftime('%Y-%b-%d')),
        l['Company'].append(company),
        l['Position'].append(job_title),
        l['Location'].append(location),
        l['Apply Here'].append(link),
        l['Posting Time'].append(posted_on.replace('via ', '')),
        l['Seniority Level'].append(req)

df = pd.DataFrame(l)
df.to_csv("hirist.csv", index=False)