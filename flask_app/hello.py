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
        # print(html)
        citeArray = countAllLinks(html)
        auth = authorNames(citeArray)
        total=int(len(citeArray))

        return render_template('index.html', name=url, array=citeArray, author=auth, all=total)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)