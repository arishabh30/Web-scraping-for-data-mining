from pickle import APPEND
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
# from fake_useragent import UserAgent

def gettingUrl(url):
    # ua=UserAgent()
    # userAgent=ua.random
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
    
def countAllLinksACS(html):
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

def TitleAcs(html):
    titleAll = []
    soup = BeautifulSoup(html,'html.parser')
    content = soup.find('ol', class_='useLabel')
    titles = content.find_all('span', class_="NLM_article-title")
    i=0
    for t in titles:
        titleAll.append(titles[i].text)
        i=i+1
    return titleAll
def AcsDoi(html):
    dois =[]
    soup = BeautifulSoup(html,'html.parser')
    content = soup.find('ol', class_='useLabel')
    doi = content.find_all('span', class_='refDoi')
    i=0
    for d in doi:
        x = re.findall("(?<=DOI\: )(.*)", doi[i].text)
        new = "https://doi.org/"
        var = ' '.join(x)
        dois.append("".join([new,var]))
        i=i+1
    return dois
def AcsYear(html):
    years =[]
    soup = BeautifulSoup(html,'html.parser')
    content = soup.find('ol', class_='useLabel')
    year = content.find_all('span', class_='NLM_year')
    i=0
    for y in year:
        years.append(year[i].text)
        i=i+1
    return years
    
def AcsJournal(html):
    journal =[]
    soup = BeautifulSoup(html,'html.parser')
    content = soup.find('ol', class_='useLabel')
    journalList = content.find_all('span', class_='citation_source-journal')
    i=0
    for j in journalList:
        journal.append(journalList[i].text)
        i=i+1
    return journal

def authorNames(citeArray,url):
    allAuthors=[]
    html = gettingUrl(url)
    count = len(citeArray)
    soup3 = BeautifulSoup(html, 'html.parser')
    content = soup3.find('ol', class_='useLabel')
    authors = content.find_all('span', class_="NLM_contrib-group")
    i=0
    for t in authors:
        allAuthors.append(authors[i].text)
        i=i+1
    return allAuthors
    # authDetail=[]
    # authArr=[]
def NatureLink(html):
    soup = BeautifulSoup(html,'html.parser')
    paperLinksgoogleScholarnature = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find('ol', class_="c-article-references")
    tags = links.find_all('a', {'data-track-action': 'google scholar reference'})
    for tag in tags:
        # creating a list containing the google scholar links for all the
        paperLinksgoogleScholarnature.append(tag['href'])

    for link in paperLinksgoogleScholarnature:
        index = paperLinksgoogleScholarnature.index(link)
        # print(index+1, link)
    return paperLinksgoogleScholarnature


def Springer(html):
    html = gettingUrl("https://link.springer.com/article/10.1007/s43673-022-00064-1")
    paperLinksgoogleScholarnature = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('ol', class_="c-article-references")
    tags = links.find_all('a', {'data-track-action': 'google scholar reference'})
    for tag in tags:
        # creating a list containing the google scholar links for all the
        paperLinksgoogleScholarnature.append(tag['href'])

    for link in paperLinksgoogleScholarnature:
        index = paperLinksgoogleScholarnature.index(link)
        print(index+1, link)

def ScienceDirect(html):
    html = gettingUrl(
    "https://www.sciencedirect.com/science/article/pii/S2376060522000608")
    paperLinksgoogleScholarelsevier = []
    paperLinkselsevierall = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('dd', class_="reference")
    for tag in tags:
        link = (tag.find_all('a', class_="link"))
        for l in link:
            paperLinkselsevierall.append(l['href'])

    for link in paperLinkselsevierall:
        if "scholar" in link:
            paperLinksgoogleScholarelsevier.append(link)

    for link in paperLinksgoogleScholarelsevier:
        index = paperLinksgoogleScholarelsevier.index(link)
        print(index+1, link)
    
def MDPI(html):
    paperLinksgoogleScholarMDPI = []
    html = gettingUrl("https://www.mdpi.com/2226-4310/9/11/704/htm")
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('ol', class_="html-xx")
    links = tags.find_all('a', class_="google-scholar")
    for link in links:
        paperLinksgoogleScholarMDPI.append(link['href'])
        index = links.index(link)
        print(index+1, link['href'])

def Science(html):
    # extraction from "Science" publication house.
    html = gettingUrl("https://science.sciencemag.org/content/371/6534/eaay9982")
    paperLinksgoogleScholarScienceall = []
    paperLinksgoogleScholarScience = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('section', {'id': 'bibliography'})
    links = tags.find_all('a')
    for link in links:
        paperLinksgoogleScholarScienceall.append(link['href'])

    for link in paperLinksgoogleScholarScienceall:
        if "scholar" in link:
            paperLinksgoogleScholarScience.append(link)
            index = paperLinksgoogleScholarScience.index(link)
            print(index+1, link)

def Ieee(html):
    html = gettingUrl(
    "https://ieeexplore.ieee.org/document/9837920/references#references")
    paperLinksgoogleScholarIEEE = []
    paperLinksgoogleScholarIEEEfinal = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('div', class_='reference-container')
    for tag in tags:
        link = tag.find('a', class_="stats-reference-link-googleScholar")
        paperLinksgoogleScholarIEEE.append(link['href'])

    initial = paperLinksgoogleScholarIEEE[0]
    paperLinksgoogleScholarIEEEfinal.append(initial)
    i = 1
    while (i < len(paperLinksgoogleScholarIEEE)):
        if paperLinksgoogleScholarIEEE[i] != initial:
            paperLinksgoogleScholarIEEEfinal.append(paperLinksgoogleScholarIEEE[i])
        else:
            break
        i += 1

    for link in paperLinksgoogleScholarIEEEfinal:
        index = paperLinksgoogleScholarIEEEfinal.index(link)
        print(index+1, link)

def Cambridge(html):
    html = gettingUrl("https://www.cambridge.org/core/journals/experimental-results/article/observing-nonuniform-nonluders-yielding-in-a-coldrolled-medium-manganese-steel-with-digital-image-correlation/1C8B6F3364BA54FC2C1D7801FCFDB85E")
    paperlinksCambridge = []
    paperlinksgoogleScholarCambridge = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('div', {'id': 'references-list'})
    links = tags.find_all('a', class_="ref-link")
    for link in links:
        paperlinksCambridge.append(link['href'])
    for link in paperlinksCambridge:
        if "scholar" in link:
            paperlinksgoogleScholarCambridge.append(link)
            index = paperlinksgoogleScholarCambridge.index(link)
            print(index+1, link)

def author_new(html):
    authors_new = []
    for link in scholarLinks:
        html = gettingUrl(link)
        # creating an instance of the BeautifulSoup library
        soup3 = BeautifulSoup(html, 'lxml')
        content = soup3.find('div', class_="gs_a")
        if content == None:
            print("No Data Found")
        else:
            authors = content.find_all('a')
            # getting the name of the professor to then set up further relationships.
            print(authors[-1].text)
            authors_new.append(authors[-1].text)
    # for link in citeArray:
    #     html = gettingUrl(link)
    #     soup3 = BeautifulSoup(html, 'html.parser')
    #     content = soup3.find('div', class_="gs_a")
    #     authors = content.find_all('a')
    #     # print(authors)
    #     authArr.append(authors[-1])
    # return authArr


def Publication(link):
    x = re.findall('www\.(.*?)\.', link)
    return x
    
    # for link in scholarLinks:
    #     html = gettingUrl(link)
    #     soup3 = BeautifulSoup(html,'html.parser')
    #     content = soup3.find('div', class_="gs_a")
    #     if content == None:
    #         print("No Data Found")
    #     else:
    #         authors = content.find_all('a')
    #         print(authors[-1].text)
    #         name = content.text
    #         if "science" in name:
    #             print("science")
    #         elif 'Wiley' in name:
    #             print("wiley")
    #         elif 'nature' in name:
    #             print("nature")
    #         elif 'sciencedirect' in name:
    #             print("sciencedirect")
    #         elif 'Springer' in name:
    #             print("Springer")
    #         elif 'Elsevier' in name:
    #             print("Elsevier")
    #         elif 'mdpi' in name:
    #             print("mdpi")
    #         elif 'ACS Publications' in name:
    #             print("ACS Publications")
    #         elif 'ieee' in name:
    #             print("ieee")
    #         else:
    #             print("other")