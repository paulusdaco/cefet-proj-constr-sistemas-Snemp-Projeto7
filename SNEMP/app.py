from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        if request.files:
            planilha = request.files["csv"]
            print(planilha)
            return redirect(request.url)
    
    return render_template("snemp.html")

if __name__ ==  "__main__":
    app.run(debug=True)