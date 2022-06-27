from flask import Flask, render_template, request, redirect
import pandas as pd
import csv
import os

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("snemp.html")

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        f = request.form["csvfile"]
        data = []
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        data = pd.DataFrame(data)
        return render_template("data.html", data = data)



if __name__ ==  "__main__":
    app.run(debug=True)