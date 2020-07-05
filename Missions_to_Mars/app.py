from flask import Flask, render_template, redirect 
import pymongo 
import scrape_mars
from flask_pymongo import PyMongo


app = Flask(__name__)


mongo = PyMongo(app=app,uri = "mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)