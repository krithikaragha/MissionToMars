from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://heroku_403zd8gs:cvv2kjnooobo9nh2n6u5ic5hfe@ds149146.mlab.com:49146/heroku_403zd8gs"
mongo = PyMongo(app)

@app.route("/")
def index():
    destination_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=destination_data)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Insert the scraped data
    mongo.db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
