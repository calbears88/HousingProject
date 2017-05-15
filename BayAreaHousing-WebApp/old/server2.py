from flask import Flask, request, send_from_directory, render_template, jsonify, redirect
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import json
import requests
import xmltodict
import csv
import sqlite3 as lite
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route("/viewseller")
def view_seller():
    
    con = lite.connect("Housing.db")
    cur = con.cursor()
    cur.execute("select Name, Phone, Email from Contact_Info")
    rows = cur.fetchall()

    return render_template("viewseller.html", **locals())


@app.route("/contact", methods=["GET", "POST"])
def add_seller():

    if request.method == "GET":
        return render_template("contact.html", **locals())

    else:
        Name = request.form["Name"]
        Phone = request.form["Phone"]
        Email = request.form["Email"]

        con = lite.connect("Housing.db")
        with con:
            cur = con.cursor()
            cur.execute("insert into Contact_Info (Name, Phone, Email) values ('{}', '{}', '{}')".format(Name, Phone, Email))     

        return redirect("/viewseller")

@app.route('/static/search.html', methods=['POST'])
def search_city():
    city1 = request.form['city1']
    city2 = request.form['city2']
    city3 = request.form['city3']
    
    return render_template("/static/results.html")

@app.route('/static/results.html', methods=['GET','POST'])
def results_page():
    con = lite.connect("Housing.db")
    cur = con.cursor()
    cur.execute("SELECT zipcode_id FROM Area WHERE primary_city =" + str(city1))
    rows = cur.fetchall()
    
    return render_template("/static/results.html")



@app.route("/search", methods=["GET", "POST"])
def city():
    
    if request.method == "GET":
        return render_template("search.html", **locals())

    else:
        city1 = request.form["city1"]

        con = lite.connect("Housing.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT ROUND(CAST(SUM(White) as FLOAT)/SUM(Total)*100,2) AS White, ROUND(CAST(SUM(Black) as FLOAT)/SUM(Total)*100,2) AS Black, ROUND(CAST(SUM(Asian) as FLOAT)/SUM(Total)*100,2) AS Asian, ROUND(CAST(SUM(Hispanic) as FLOAT)/SUM(Total)*100,2) AS Hispanic FROM Race_ethnicity, AREA  WHERE zipcode_id=Zipcode")

    return render_template("viewcity.html", **locals())



if __name__ == "__main__":
    app.run()

