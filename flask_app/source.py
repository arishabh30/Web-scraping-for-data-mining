import PyPDF2
import re
import requests
import time
import array as arr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import request
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def gettingUrl(url):
    ua=UserAgent()
    userAgent=ua.random
    options = Options()
    options.headless=True
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--lang=en_US')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=[userAgent]")
    options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)
    html = browser.page_source
    print("URL "+url)
    return html

def gettingRef(html,ref):
    soup_new = BeautifulSoup(html.text,'html.parser')  #creating an instance of the BeautifulSoup library
    a_tags = soup_new.find('div', class_="article_content-left ui-resizable")
    count = a_tags.find_all('a',class_="ref{}".format(ref))
    len_count = len(count)
    return len_count
    
def countAllLinks(html):
    soup2 = BeautifulSoup(html,'html.parser')
    a_tags = soup2.find('div', class_="article_content-left ui-resizable")
    paperLinksgoogleScholar=a_tags.find_all('a',class_="google-scholar")  # creating a list containing the google scholar links for all the reference papers.
    scholarLinks=[]
    for link in paperLinksgoogleScholar:
        scholarLinks.append(link['href'])  #A new list containing the google scholar links for only the first three papers is created. 
    return scholarLinks

def paperName(array):
    browser = webdriver.Chrome()
    names=[]
    for link in array:
        browser.get(link)
        time.sleep(5)
        browser.find_element(By.LINK_TEXT, "Cite").click()
        browser.get(browser.current_url)
        html = browser.page_source
        soup4 = BeautifulSoup(html, 'html.parser')
        paperName = soup4.find('div',class_ = 'gs_citr')
        name = paperName
        names.append(name)
    return names

def authorNames(citeArray):
    authDetail=[]
    authArr=[]
    for link in citeArray:
        html = gettingUrl(link)
        soup3 = BeautifulSoup(html, 'html.parser')
        content = soup3.find('div', class_="gs_a")
        authors = content.find_all('a')
        # print(authors)
        authArr.append(authors[-1])
    return authArr

# def authorName(scholarLinks):
#     for link in scholarLinks:
#         html = gettingUrl(link)
#         soup3 = BeautifulSoup(html,'html.parser')
#         content = soup3.find('div', class_="gs_a")

#         if content == None:
#             print("No Data Found")
#         else:
#             authors = content.find_all('a')
#             print(authors[-1].text)
#             name = content.text
#             if "science" in name:
#                 print("science")
#             elif 'Wiley' in name:
#                 print("wiley")
#             elif 'nature' in name:
#                 print("nature")
#             elif 'sciencedirect' in name:
#                 print("sciencedirect")
#             elif 'Springer' in name:
#                 print("Springer")
#             elif 'Elsevier' in name:
#                 print("Elsevier")
#             elif 'mdpi' in name:
#                 print("mdpi")
#             elif 'ACS Publications' in name:
#                 print("ACS Publications")
#             elif 'ieee' in name:
#                 print("ieee")
#             else:
#                 print("other")