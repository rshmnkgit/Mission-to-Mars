#!/usr/bin/env python
# coding: utf-8

# Import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    # Activate the chrome browser
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

######    NASA Mars News    ########################################
def scrape_marsnews():
    browser = init_browser()
    # Open the nasa website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)    

    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    news_article = soup.find('li', class_='slide')
    # Scrape the date of publishing the news
    news_date = news_article.find('div', class_='list_date').text
    # Scrape the news title
    news_title = news_article.find('div', class_="content_title").text
    # Scrape the news paragraph
    news_para = news_article.find('div', class_="article_teaser_body").text
    browser.quit()
    return [news_title, news_para]



######    JPL Mars Space Images    ########################################
def scrape_jplimage():

    browser = init_browser()
    # Open the jpl.nasa.gov/spaceimages webpage
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # button = browser.click_link_by_partial_text('FULL IMAGE')
    button = browser.find_by_id('full_image', wait_time=1)
    button.click()
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')
    jpl_image = soup.find('figure', class_="lede")
    main_image = jpl_image.find('img', class_='main_image')
    image_src = main_image['src']
    featured_image_src = "https://www.jpl.nasa.gov/" + image_src    
    browser.quit()
    return featured_image_src


#####   Mars Facts    ###############################################
def scrape_marsfacts():
    # Got ot the web page https://space-facts.com/mars/
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    marsfact = tables[0]
    marsfact.columns = ['Description', 'Units']
    facts_dictionary = marsfact.to_dict("records")
    return facts_dictionary


#####  Mars Hemisphere  #################################################
def scrape_hemisphere():
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Loop through the images
    hemisphere_image_urls = []

    for item in range(4):
        browser.find_by_tag('h3')[item].click()
        time.sleep(2)
        
        html = browser.html
        soup = bs(html, 'html.parser')

        imgsrc = soup.find('img', class_='wide-image')
        source = imgsrc['src']

        image_url = "https://astrogeology.usgs.gov" + source
        image_title = soup.find('h2').text
        browser.back()    
        hemisphere_image_urls.append({'img_url':image_url, 'title':image_title})

    hemisphere_image_urls    
    browser.quit()
    return hemisphere_image_urls