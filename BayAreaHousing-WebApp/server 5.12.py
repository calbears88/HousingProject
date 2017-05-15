from flask import Flask, request, render_template
import sqlite3 as lite
import sample
import json
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template('index.html')


@app.route("/search")
def search_city():
    return render_template("search.html")


@app.route("/results", methods=["GET", "POST"])
def results_page():

    if request.method == "POST":
        city_one = request.form["city1"]

        con = lite.connect("Housing.db")
        cur = con.cursor()
        cur.execute("SELECT zipcode_id, primary_city, county FROM Area WHERE primary_city = ?", (city_one,))
        rows = cur.fetchall()
        return render_template("results.html", **locals())


@app.route("/yelp_search")
def search_yelp():
    return render_template("yelp_search.html")


@app.route("/yelp_results", methods=["GET", "POST"])
def results_yelp():

    if request.method == "POST":
        search_term = request.form["yelp_search"]
        city_term = request.form["yelp_city"]
        
        yelp_response = sample.query_yelp_search(search_term,city_term)
        
        yelp_data = json.dumps(yelp_response)
        yelp_json = json.loads(yelp_data)
        yelp_bus = yelp_json['businesses']
        names = []
        price = []
        rating = []
        genre = []
        rank = []
        for i in range(len(yelp_bus)):
            rank.append(i+1)
            names.append(yelp_bus[i]['name'])
            price.append(yelp_bus[i]['price'])
            rating.append(yelp_bus[i]['rating'])
            genre.append(yelp_bus[i]['categories'][0]['title'])

        full_list = [rank,names,genre,price,rating]
        full_list_T = list(map(list, zip(*full_list)))
#        full_frame = pd.DataFrame({'Names':names,'Price':price,'Rating':rating,'Title':genre})

        return render_template("yelp_results.html", **locals())


if __name__ == "__main__":
    app.run()