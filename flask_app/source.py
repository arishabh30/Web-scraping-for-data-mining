from pickle import APPEND
# import pandas as pd
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
    options.headless = True
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--lang=en_US')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=[userAgent]")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    browser.get(url)
    html = browser.page_source
    # currentURL = browser.current_url
    print("URL "+url)
    return html

def convert_to_actual_url(doi_url): 
    options = Options()
    options.headless = True
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--lang=en_US')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=[userAgent]")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(doi_url)

    time.sleep(5)

    return driver.current_url

def Nature(html):
    # Extraction from "Nature" publication house.
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find('ol', class_="c-article-references")
    tags = links.find_all(
        'a', {'data-track-action': 'google scholar reference'})
    # to get the google scholar links of the references.
    paperLinksgoogleScholarnature = []
    for tag in tags:
        # creating a list containing the google scholar links for all the
        paperLinksgoogleScholarnature.append(tag['href'])

    # to get the doi of the references.
    natureDOI = []
    refNumber = len(paperLinksgoogleScholarnature)

    i = 0

    for i in range(1, int(refNumber)+1):
        doiLinks = links.find('a', {'aria-label': 'Article reference '+str(i)})

        if doiLinks == None:
            natureDOI.append("No DOI")
        else:
            natureDOI.append(doiLinks['href'])
        i += 1

    # extracting the authors from the main page itself.
    text = soup.find_all('ol', class_='c-article-references')
    # print(text)
    text_main = soup.find_all(
        'li', class_='c-article-references__item js-c-reading-companion-references-item')
    # print(text_main[0])

    Titles = []
    allLastAuthors = []
    journalName = []
    yearPublication = []

    for ref in text_main:
        string = ref.find('p', class_='c-article-references__text')

        togetdeets = string.text.split('.')

        # returns authors in the form of a string.
        allAuthors = togetdeets[0]
        allAuthorsList = allAuthors.split(',')  # converting to a list

        Titles.append(togetdeets[1])  # gets the title of the references

        journal = togetdeets[2].split(';')
        # gets the journal name of the references
        journalName.append(journal[0])

        if len(togetdeets) < 4:
            # gets the year of publication of the references
            yearPublication.append(' ')
        else:
            year = togetdeets[3].split(';')
            # gets the year of publication of the references
            yearPublication.append(year[0])

        if allAuthorsList[-1] == ' et al':
            allLastAuthors.append(allAuthorsList[-2])
        else:
            allLastAuthors.append(allAuthorsList[-1])

    return allLastAuthors, Titles, journalName, yearPublication, natureDOI, paperLinksgoogleScholarnature


def Springer(html):
    # Extraction from "Springer" publication house.
    # html = gettingUrl("https://link.springer.com/article/10.1007/s43673-022-00064-1")
    paperLinksgoogleScholar = []

# creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('ol', class_="c-article-references")
    refNumber = len(links)
    k = 0
    for k in range(1, int(refNumber)+1):
        tags = links.find(
            'a', {'aria-label': 'Google Scholar reference ' + str(k)})
        if tags == None:
            paperLinksgoogleScholar.append("No Google Scholar Link")
        else:
            paperLinksgoogleScholar.append(tags['href'])
        k += 1

    # to get the doi of the references.
    springerDOI = []

    i = 0

    for i in range(1, int(refNumber)+1):
        doiLinks = links.find('a', {'aria-label': 'Article reference '+str(i)})

        if doiLinks == None:
            springerDOI.append("No DOI")
        else:
            springerDOI.append(doiLinks['href'])
        i += 1

    # print(springerDOI)

    # extracting the authors from the main page itself.
    text = soup.find_all('ol', class_='c-article-references')
    text_main = soup.find_all(
        'li', class_='c-article-references__item js-c-reading-companion-references-item')

    Titles = []
    allLastAuthors = []
    journalName = []
    yearPublication = []

    for ref in text_main:
        string = ref.find('p', class_="c-article-references__text")

        togetdeets = string.text.split(',')
        content = togetdeets[-2].split('.')
        Titles.append(content[0])  # gets the title of the references

        if len(togetdeets) < 4:
            allLastAuthors.append("No Data Found")
        else:
            allLastAuthors.append(togetdeets[-3])

        sum = ''
        for j in range(1, len(content)-1):
            sum += content[j]
        journalName.append(sum)  # gets the journal name of the references

        year = togetdeets[-1].split('(')
        # print(year[-1])

        if year[-1][0] == " ":
            # gets the year of publication of the references
            yearPublication.append("No Data Found")
        else:
            year_new = year[-1].split(')')
            # gets the year of publication of the references
            yearPublication.append(year_new[0])

    return allLastAuthors, Titles, journalName, yearPublication, springerDOI, paperLinksgoogleScholar


def Science(html):
    # extraction from "Science" publication house.
    # html = gettingUrl("https://www.science.org/doi/10.1126/sciadv.abq2104")
    paperLinksgoogleScholar = []
    scienceDOI = []
    toGetDeets = []
    allLastAuthors = []
    journalName = []
    Titles = []
    yearPublication = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('section', {'id': 'bibliography'})
    forLabels = tags.find_all("div", class_='label')

    refNumber = len(forLabels)

    i = 0

    content = tags.find_all('div', class_="citation")
    for con in content:
        toGetDeets.append(con.find('div', class_='citation-content'))

    for deet in toGetDeets:
        if deet.find('em') == None:
            journalName.append("No Data Found")
        else:
            journalName.append(deet.find('em').text)

    for deet in toGetDeets:
        detail = deet.text.split(',')
        if ('(' in detail[-1]) == False:
            yearPublication.append("No Data Found")
        else:
            yearPublication.append(detail[-1].split('(')[-1].split(')')[0])

    for deet in toGetDeets:
        Titles.append(deet.text)

    for con in content:
        link = con.find('a')
        if link.text == "Crossref":
            scienceDOI.append(link['href'])
        else:
            scienceDOI.append("No DOI")

    for con in content:
        link = con.find_all('a')
        if (link[-1].text == "Google Scholar"):
            paperLinksgoogleScholar.append(link[-1]['href'])
        else:
            paperLinksgoogleScholar.append("Google Scholar Link Not Found")

    for i in range(0, refNumber):
        allLastAuthors.append("Next Column for Authors")

    return allLastAuthors, Titles, journalName, yearPublication, scienceDOI, paperLinksgoogleScholar


def MDPI(html):
    paperLinksgoogleScholar = []
    toGetDeets = []
    Titles = []
    mdpiDOI = []
    allLastAuthors = []
    journalName = []
    yearPublication = []
    # html = gettingUrl("https://www.mdpi.com/2226-4310/9/11/704/htm")
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('ol', class_="html-xx")

    refNumber = len(tags)

    i = 0

    for i in range(1, int(refNumber)+1):
        content = tags.find('li', {'data-content': "{}".format(i)+'.'})

        forName = content.find('span', class_="html-italic")

        if forName == None:
            journalName.append("No Data Found")
        else:
            journalName.append(forName.text)

        forYear = content.find('b')

        if forYear == None:
            yearPublication.append("No Data Found")
        else:
            yearPublication.append(forYear.text)

        toGetDeets.append(content.text.split('[')[0])

        if "CrossRef" in content.text:
            mdpiDOI.append(content.find('a', class_='cross-ref')['href'])
        else:
            mdpiDOI.append("DOI not found")

        if "Google Scholar" in content.text:
            paperLinksgoogleScholar.append(content.find(
                'a', class_='google-scholar')['href'])
        else:
            paperLinksgoogleScholar.append("Google Scholar Link not found")

    for deet in toGetDeets:
        detail = deet.split(';')[-1]
        allLastAuthors.append(detail.split('.')[0])
        Titles.append(detail.split('.')[:-2])

    return allLastAuthors, Titles, journalName, yearPublication, mdpiDOI, paperLinksgoogleScholar


def IEEE(html):
    # html = gettingUrl("https://ieeexplore.ieee.org/document/9837920/references#references")
    paperLinksgoogleScholar = []

    ieeeDOI = []
    allLastAuthors = []
    journalName = []
    Titles = []
    yearPublication = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('div', class_='reference-container')
    for tag in tags:

        detail = tag.find('div', class_="col u-px-1")
        fineDetail = detail.find('div')

        if fineDetail.find('em') == None:
            journalName.append("No Data Found")
        else:
            journalName.append(fineDetail.find('em').text)

        Titles.append(fineDetail.text.split('"')[-1])

        if 'and' in fineDetail.text.split('"')[0]:
            allLastAuthors.append(fineDetail.text.split('"')[
                                  0].split('and')[-1])
        else:
            allLastAuthors.append(fineDetail.text.split('"')[0])

        yearPublication.append(fineDetail.text.split('"')[-1].split('.')[-2])

        doi = tag.find('a', class_="stats-reference-link-crossRef")
        doi_ieee = tag.find('a', class_="stats-reference-link-viewArticle")

        if doi == None and doi_ieee == None:
            ieeeDOI.append("No DOI")
        elif doi == None:
            ieeeDOI.append("https://ieeexplore.ieee.org"+doi_ieee['href'])
        else:
            ieeeDOI.append(doi['href'])

        gscholar = tag.find('a', class_="stats-reference-link-googleScholar")
        if gscholar == None:
            paperLinksgoogleScholar.append("Google Scholar Link Not Found")
        else:
            paperLinksgoogleScholar.append(gscholar['href'])

    return allLastAuthors, Titles, journalName, yearPublication, ieeeDOI, paperLinksgoogleScholar


def Cambridge(html):
    # extraction from "Cambridge publishing house" publication house.
    # html = gettingUrl("https://www.cambridge.org/core/journals/advances-in-archaeological-practice/article/professionalcollector-collaboration/8DB3D024A682DEC74457D6D5708B8D73")
    paperlinksgoogleScholar = []
    content_list = []
    allLastAuthors = []
    Titles = []
    yearPublication = []
    journalName = []
    cambridgeDOI = []
    allAuthors = []

    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('div', {'id': 'references-list'})
    for tag in tags:
        content_list.append(tag)

    content = content_list[3:]
    refNumber = len(content)

    i = 0

    for i in range(2, refNumber+2):
        toGetDeets = content[i-2].find('div',
                                       {'id': 'reference-'+"{}".format(i)+'-content'})

        link = toGetDeets.find('a', class_='ref-link')
        links = toGetDeets.find_all('a', class_='ref-link')
        if link.text == "CrossRef":
            cambridgeDOI.append(link['href'])
        else:
            cambridgeDOI.append("No DOI")

        if links[-1].text == "Google Scholar":
            paperlinksgoogleScholar.append(links[-1]['href'])
        else:
            paperlinksgoogleScholar.append(
                "Google Scholar Link Not Found")

            yearPublication.append(toGetDeets.find('span', class_='year').text)

        if toGetDeets.find('span', class_='article-title') != None:
            Titles.append(toGetDeets.find('span', class_='article-title').text)
        else:
            Titles.append("No data found")

        if toGetDeets.find('span', class_='publisher-name') != None:
            journalName.append(toGetDeets.find(
                'span', class_='publisher-name').text)
        elif toGetDeets.find('span', class_='source') != None:
            journalName.append(toGetDeets.find('span', class_='source').text)
        else:
            journalName.append("No Data Found")

        # print(toGetDeets)
        author = toGetDeets.find_all('span', class_='string-name')
        allAuthors.append(author)

    for auth in allAuthors:
        if auth == []:
            allLastAuthors.append("No Data Found")
        elif len(auth) == 1:
            allLastAuthors.append(auth[0].text)
        else:
            allLastAuthors.append(auth[-1].text)

    return allLastAuthors, Titles, journalName, yearPublication, cambridgeDOI, paperlinksgoogleScholar


def ScienceDirect(html):
    # extraction from "Elsevier(sciencedirect)" publication house.
    # html = gettingUrl("https://www.sciencedirect.com/science/article/pii/S2376060522000608")
    paperLinksgoogleScholar = []
    Titles = []
    scienceDirectDOI = []
    journalName = []
    links = []
    allLastAuthors = []
    yearPublication = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('dd', class_="reference")

    refNumber = len(tags)

    i = 0

    for i in range(1, int(refNumber)+1):
        tag = soup.find('dd', {'id': 'sref'+"{}".format(i)})
        Titles.append(tag.find('strong', class_="title").text)
        journalName.append(tag.find('div', class_="host").text)
        yearPublication.appendtag.find('div', class_="host").text.split(
            ',')[-2].split('(')[-1].split(')')[0]
        links = tag.find_all('a', class_="link")
        if links[0].text == "Article":
            scienceDirectDOI.append(
                "https://www.sciencedirect.com/"+links[0]['href'])
        else:
            scienceDirectDOI.append("No DOI")

        if links[-1].text == "Google Scholar":
            paperLinksgoogleScholar.append(links[-1]['href'])
        else:
            paperLinksgoogleScholar.append("No Google Scholar Link")

        content = tag.find('div', class_="contribution").text.split(',')
        if "et al" in content[-1]:
            allLastAuthors.append(content[-2])
        else:
            allLastAuthors.append(content[-1].replace(Titles[i-1], " "))
        i += 1
    return allLastAuthors, Titles, journalName, yearPublication, scienceDirectDOI, paperLinksgoogleScholar


def ACS(html):
    # extraction from "ACS" publication house.
    paperlinksgoogleScholar = []
    allLastAuthors = []
    Titles = []
    yearPublication = []
    journalName = []
    acsDOI = []
    DOI = []
    authors = []
    # html = gettingUrl("https://pubs.acs.org/doi/10.1021/acsnano.5b05040")
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find("ol", class_="useLabel")

    refNumber = len(tags)

    i = 0

    for i in range(1, int(refNumber)+1):
        toGetDeets = tags.find('li', {'id': 'ref'+'{}'.format(i)})
        content = toGetDeets.find('div', {'id': 'cit'+'{}'.format(i)})
        if content == None:
            allLastAuthors.append("No Data Found")
            Titles.append("No Data Found")
            yearPublication.append("No Data Found")
            journalName.append("No Data Found")
            DOI.append("No DOI")
            authors.append("No Data Found")
            paperlinksgoogleScholar.append("Google Scholar Link Not Found")
        else:
            authors.append(content.find_all(
                'span', class_='NLM_contrib-group'))
            allLastAuthors.append(authors[i-1][-1].text)
            Titles.append(content.find(
                'span', class_='NLM_article-title').text)
            journalName.append(content.find(
                'span', class_='citation_source-journal').text)
            yearPublication.append(content.find(
                'span', class_='NLM_year').text)
            DOI.append(content.find('span', class_='refDoi').text)

            paperlinksgoogleScholar.append(content.find(
                'a', class_='google-scholar')['href'])

    j = 0
    for link in DOI:
        if link == "No DOI":
            acsDOI.append("No DOI")
        else:
            x = re.findall("(?<=DOI\: )(.*)", DOI[j])
            new = "https://doi.org/"
            var = ' '.join(x)
            acsDOI.append("".join([new, var]))
        j += 1
    return allLastAuthors, Titles, journalName, yearPublication, acsDOI, paperlinksgoogleScholar


def Publication(link):
    x = re.findall('www\.(.*?)\.', link)
    return x
