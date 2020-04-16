from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #News
    news_url = 'https://mars.nasa.gov/news/'
    news_response = requests.get(news_url)
    news_soup = BeautifulSoup(news_response.text, 'html.parser')
    news_title = news_soup.find('div', class_="content_title").text
    news_p = news_soup.find('div', class_="rollover_description").text

    #Featured Image
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    
    browser.click_link_by_partial_text('FULL IMAGE')

    browser.click_link_by_partial_text('more info')

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    featured_image_path = img_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_path}'

    #Tweeter
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    tweet_response = requests.get(tweet_url)
    tweet_soup = BeautifulSoup(tweet_response.text, 'html.parser')

    mars_weather = tweet_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #Facts
    facts_url = 'https://space-facts.com/mars/'

    table = pd.read_html(facts_url)

    df = table[0]
    df.columns = ['Description', 'Value']

    html_table = df.to_html(classes = 'table table-striped')

    #Hemishperes
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_response = requests.get(hem_url)
    hem_soup = BeautifulSoup(hem_response.text, 'html.parser')

    results = hem_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for result in results:
    
        title = result.find('h3').text
        single_url = 'https://astrogeology.usgs.gov' + result.find('a', class_='itemLink product-item')['href']
        single_response = requests.get(single_url)
        single_soup = BeautifulSoup(single_response.text, 'html.parser')
    
        img_url = single_soup.find('img', class_='wide-image')['src']
    
        hemisphere_image_urls.append({"title" : title, "img_url" : f'https://astrogeology.usgs.gov{img_url}'})
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data