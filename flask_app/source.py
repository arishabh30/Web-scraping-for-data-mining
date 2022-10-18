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
from hello import index
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def gettingUrl(url):
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
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)
    html = browser.page_source
    print("URL " +url)
    return html

def gettingRef(html,ref):
    soup_new = BeautifulSoup(html,'html.parser')  #creating an instance of the BeautifulSoup library
    a_tags = soup_new.find('div', class_="article_content-left ui-resizable")
    count = a_tags.find_all('a',class_="ref{}".format(ref))
    len_count = len(count)
    return len_count

def refLinks(html):
    soup2 = BeautifulSoup(html,'html.parser')  #creating an instance of the BeautifulSoup library
    links = soup2.find('div', class_="article_content-left ui-resizable")
    paperLinksgoogleScholar=links.find_all('a',class_="google-scholar")  # creating a list containing the google scholar links for all the reference papers.
    index=0
    scholarLinks=[]
    for link in paperLinksgoogleScholar:
        scholarLinks.append(link['href'])  #A new list containing the google scholar links for only the first three papers is created. 
        index=index+1
    return scholarLinks
    
def countCite(html,val):
    soup2 = BeautifulSoup(html,'html.parser')
    a_tags = soup2.find('div', class_="article_content-left ui-resizable")
    paperLinksgoogleScholar=a_tags.find_all('a',class_="google-scholar")  # creating a list containing the google scholar links for all the reference papers.
    index=0
    scholarLinks=[]
    for link in paperLinksgoogleScholar:
        scholarLinks.append(link['href'])  #A new list containing the google scholar links for only the first three papers is created. 
        index=index+1
    index = 1
    citeArray=[]
    for link in scholarLinks:
        count = len(a_tags.find_all('a',class_="ref{}".format(index)))
        if int(count) >= int(val):
            citeArray.append(link)
    return citeArray

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

def autherNames(citeArray):
    authDetail=[]
    for link in citeArray:
        html = gettingUrl(link)
        soup3 = BeautifulSoup(html, 'html.parser')
        content = soup3.find('div', class_="gs_a")
        # authors = content.find_all('a')
        # authArr=[]
        # # print(authors)
        # for author in authors:
        #     authArr.append(author.text)
        
        authDetail.append(content)
    return authDetail





    