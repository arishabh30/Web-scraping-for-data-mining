from flask import Flask, render_template, url_for, request
from source import *
import csv
import numpy as np
import pandas as pd
app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("enteredurl")
        print(url)
        # val = request.form.get("cite")
        # gettingUrl("https://pubs.acs.org/doi/10.1021/acsnano.9b06394")
        html = gettingUrl(url)
        print(html)

        #getting the if check

        string = url.split(".")

        if "springer" in string:
            auth, titles, journalList, yearlist, DOIs, scholarLinks = Springer(html)
        
        elif "nature" in string:
            auth, titles, journalList, yearlist, DOIs, scholarLinks = Nature(html) 

        elif "science" in string:
            auth, titles, journalList, yearlist, DOIs, scholarLinks = Science(html)

        elif "mdpi" in string:
            auth, titles, journalList, yearlist, DOIs, scholarLinks = MDPI(html)

        elif "ieee" in string:
            url = url + "/references#references"
            auth, titles, journalList, yearlist, DOIs, scholarLinks = IEEE(html)

            # auth, titles, journalList, yearlist, DOIs, scholarLinks = Nature(html)
            
        # citeArray = countAllLinksACS(html)
        # auth = authorNames(citeArray,url)
        # # print(auth)
        # titles = TitleAcs(html)
        # DOIs = AcsDoi(html)
        # # print(titles)
        # total=int(len(citeArray))
        # yearlist = AcsYear(html)
        # journalList = AcsJournal(html)


        

        

        # dict = {'Author':auth,'Title':titles,'Journal':journalList,'Year of publication':yearlist,'DOI number':DOIs,'Scholar Links':scholarLinks}

        # df = pd.DataFrame(dict) 
        # # saving the dataframe 
        # df.to_csv('content.csv') 
            
      
        
        

        return render_template('index.html', name=url, author=auth, titleAll = titles,DOIList =DOIs, YearList = yearlist, journals = journalList, array = scholarLinks)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)