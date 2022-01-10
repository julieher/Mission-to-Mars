# 1. Use Flask to render a template, redirecting to another url, and creating a URL
# 2. Use PyMongo to interact with our Mongo database
# 3. Use the scraping code, we will convert from Jupyter notebook to Python.

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# This route tells Flask what to display when we're looking at the home page
@app.route("/")

def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Scraping route
@app.route("/scrape")

def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   # .update_one(query_parameter, {"$set": data}, options)
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()