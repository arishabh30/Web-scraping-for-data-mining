from flask import Flask, render_template, url_for, request
from source import *

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
        citeArray = countAllLinksACS(html)
        auth = authorNames(citeArray,url)
        # print(auth)
        titles = TitleAcs(html)
        DOIs = AcsDoi(html)
        # print(titles)
        total=int(len(citeArray))
        yearlist = AcsYear(html)
        journalList = AcsJournal(html)
        # x = Publication(url)
        # print(x)
        # # citeArray=[]
        # auth=[]
        # titles=[]
        # DOIs=[]
        # yearlist=[]
        # journalList=[]
        # total = 0
        # if(x=='pubs'):
        #     citeArray = countAllLinksACS(html)
        #     auth = authorNames(citeArray,url)
        #     # print(auth)
        #     titles = TitleAcs(html)
        #     DOIs = AcsDoi(html)
        #     # print(titles)
        #     total=int(len(citeArray))
        #     yearlist = AcsYear(html)
        #     journalList = AcsJournal(html)
        # elif(x=='nature'):
            
      
        
        

        return render_template('index.html', name=url, array=citeArray, author=auth, all=total, titleAll = titles,DOIList =DOIs, YearList = yearlist, journals = journalList)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)