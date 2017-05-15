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

@app.route("/search", methods=["GET", "POST"])
def search_city():

    if request.method == "GET":
        return render_template("search.html", **locals())

    else:
        Name = request.form["city1"]
        Phone = request.form["city2"]
        Email = request.form["city3"]

        con = lite.connect("Housing.db")
        with con:
            cur = con.cursor()
            cur.execute("select Name, Phone, Email from Contact_Info")     

        return redirect("/results")

@app.route("/results")
def results_page():

    con = lite.connect("Housing.db")
    cur = con.cursor()
    cur.execute("select Name, Phone, Email from Contact_Info")
    rows = cur.fetchall()
            
    return render_template("results.html", **locals())




if __name__ == "__main__":
    app.run()