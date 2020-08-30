from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_missonmars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/test_mars_db")
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    try:
        # Find one record of data from the mongo database
        destination_data = mongo.db.marscollection.find_one()
    except:
        print("Database Not Found")
        # Return template and data
    return render_template("index.html", mars_html=destination_data)
    

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_news = scrape_missonmars.scrape_marsnews()
    jpl_imageurl = scrape_missonmars.scrape_jplimage()
    hemisphere_list = scrape_missonmars.scrape_hemisphere()
    marsfact_dict = scrape_missonmars.scrape_marsfacts()

    # mars_dictionary = {'news_title':mars_news[0], 'news_para':mars_news[1], 
    #                     'jpl_image':jpl_img,
    #                     hemi_list }
    print(f"\n----------------------------")
    # print(mars_dictionary)
    print(f"news  {mars_news}")
    print(f"img src   {jpl_imageurl} ")
    print(f"hemisp  {hemisphere_list}")
    print(marsfact_dict)
    print("-------------------------------\n")

    mars_dictionary = {'news_title':mars_news[0], 'news_para':mars_news[1], 
                        'jpl_image':jpl_imageurl,
                        'hemisphere':hemisphere_list,
                        'mars_data':marsfact_dict
                        }

    # Update the Mongo database using update and upsert=True
    mongo.db.marscollection.update({}, mars_dictionary, upsert=True)    

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)