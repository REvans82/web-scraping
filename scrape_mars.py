# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    titles, para = news(browser)
    results = {
        "news_title": titles,
        "news_paragraph": para,
        "featured_image_url": feature(browser),
        "mars_facts": facts(),
        "mars_hemispheres": hemi(browser)
    }

    browser.quit()
    return results

def news(browser):
    url = "https://redplanetscience.com/"
    # initiating the webdriver for instant Chrome browser
    browser.visit(url)
    # web page content
    html = browser.html
    # parsing html using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select_one("div.list_text")
    titles = results.find("div", class_="content_title").text
    para = soup.find("div", class_="article_teaser_body").text
    return titles, para

def feature(browser):
    url_jpl = "https://spaceimages-mars.com/"
    # initiating the webdriver for instant Chrome browser
    browser.visit(url_jpl)
    # web page content
    html = browser.html
    # parsing html using BeautifulSoup
    soup_jpl = BeautifulSoup(html, 'html.parser')
    # Featured Space Image Site
    image_path = soup_jpl.find("img",class_="headerimage fade-in").get("src")      
    featured_image_url = url_jpl+image_path
    return featured_image_url

def facts():
    url_mars = "https://galaxyfacts-mars.com"
    # Use Pandas to convert the data to a HTML table string
    mars_df = pd.read_html(url_mars)
    # Use Pandas to scrape the table containing facts about the planet 
    current_feature_df = mars_df[0]
    new_header = current_feature_df.iloc[0] #grab the first row for the header
    current_feature_df = current_feature_df[1:] #take the data less the header row
    current_feature_df.columns = new_header #set the header row as the df header
    current_feature_df = current_feature_df.set_index(["Mars - Earth Comparison"])
    return current_feature_df.to_html(classes="table table-striped")


def hemi(browser):
    url_hemi = "https://marshemispheres.com/"
    # initiating the webdriver for instant Chrome browser
    browser.visit(url_hemi)
    hemisphere_image_urls = []
    img_list = browser.find_by_css("a.itemLink.product-item img")
    for i in range(len(img_list)):
        full_dict = {}
        browser.find_by_css("a.itemLink.product-item img")[i].click()
        full_dict['title'] = browser.find_by_css("h2.title").text
        sample_button = browser.find_by_text("Sample")
        sample_button.click()
        full_dict['img_url'] = sample_button['href'] #browser.find_by_css('img')[0]['src']
        hemisphere_image_urls.append(full_dict)
        browser.back()  
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())