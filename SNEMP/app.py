from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = "static/Excel"
app.secret_key = "123"

con=sqlite3.connect("MyData.db")
con.execute("create table if not exists data(pid integer primary key, exceldata TEXT)")
con.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        csvfile = request.files['csvfile']
        if csvfile.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], csvfile.filename)
            csvfile.save(filepath)
            con = sqlite3.connect("MyData.db")
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)", (csvfile.filename,))
            con.commit()

            con = sqlite3.connect("MyData.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from data")
            data = cur.fetchall()
            con.close
            return render_template("snemp.html", data=data)

    if request.method == "GET":
        con = sqlite3.connect("MyData.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from data")
        data = cur.fetchall()
        con.close
        return render_template("snemp.html", data=data)

    return render_template("snemp.html")

@app.route('/bd/<string:id>')
def bd(id):
    con = sqlite3.connect("MyData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data where pid=?",(id))
    data = cur.fetchall()
    for val in data:
        path = os.path.join("static/Excel/",val[1])
        data = pd.read_csv(path)
    numrow = len(data)
    con.close()
    # return render_template("bd.html", value = numrow, data = data.to_html(index=False, classes="table table-bordered text-white center").replace('<th>','<th class="align-middle" style="text-align:center">'))
    return render_template("bd.html", value = numrow)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("MyData.db")
        cur = con.cursor()
        cur.execute("delete from data where pid=?",(id))
        con.commit()
    finally:
        return redirect(url_for("index"))
        con.close()

    
if __name__ ==  "__main__":
    app.run(debug=True)