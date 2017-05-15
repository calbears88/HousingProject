from flask import Flask, request, render_template, redirect
import sqlite3 as lite

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


if __name__ == "__main__":
    app.run()