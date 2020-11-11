from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo 
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    scrape_mars = mongo.db.collection.find_one()
    return render_template("index.html", mars = scrape_mars)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    scrape_mars = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scrape_mars, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)