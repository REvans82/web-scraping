from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mtm_app"
mongo = PyMongo(app)

# Initialize route

@app.route("/")
def index():
    mars_web = mongo.db.mars_web.find_one()
    return render_template("index.html", mars_web=mars_web)

# Route to trigger scraping
@app.route("/scrape")
def scrape():
    mars_web = mongo.db.mars_web
    mars_app = scrape_mars.scrape()
    mars_web.update({}, mars_app, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
