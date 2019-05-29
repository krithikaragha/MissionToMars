import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # Scrape Mars News
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    news_soup = bs(response.text, 'lxml')

    news_title = news_soup.find('div', class_='content_title').text.strip()

    news_p = news_soup.find('div', class_='rollover_description_inner').text

    # Scrape Featured Image
    imgUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imgUrl)

    html = browser.html
    featured_img_soup = bs(html, 'html.parser')

    jpl_base_url = 'https://www.jpl.nasa.gov'

    img_url = featured_img_soup.find("a", {"class":"button fancybox"})['data-fancybox-href']

    featured_img_url = jpl_base_url + img_url

    # Scrape Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    weather_soup = bs(response.text, 'lxml')

    li_tags = weather_soup.findAll('li', class_='js-stream-item stream-item stream-item')

    div_content = li_tags[0].find('div', class_='content')
    div_tweet = div_content.find('div', class_='js-tweet-text-container')
    
    mars_weather = div_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # Scrape Mars Facts
    facts_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(facts_url, encoding='utf-8')

    facts_df = tables[0]
    facts_df = facts_df.T
    facts_df = facts_df.iloc[1:]
    facts_df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
                        'Orbital Distance', 'Orbital Period', 'Surface Temperature', 
                        'First Record', 'Recorded By']

    facts_table = facts_df.to_html()

    # Scrape Mars Hemispheres
    hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(hems_url)
    hems_soup = bs(response.text, 'lxml')

    links = []      # List to store the links to be visited
    hemisphere_img_urls = []    # Links to store the dictionaries for each hemisphere
    astro_base_url = "https://astrogeology.usgs.gov"

    div_result = hems_soup.find('div', class_='result-list')
    div_items = div_result.findAll('div', class_='item')

    for div_item in div_items:
        hemisphere = {}
        div_content = div_item.find('div', class_='description')
    
        title = div_content.find('h3').text
        hemisphere["title"] = title

        href = div_item.find('a', {"class":"itemLink product-item"})['href']
        links.append(astro_base_url + href)

        for link in links:
            response = requests.get(link)
            link_soup = bs(response.text, 'lxml')

            img_src = link_soup.find("img", {"class":"wide-image"})['src']
            img_url = astro_base_url + img_src
            hemisphere["img_url"] = img_url

        hemisphere_img_urls.append(hemisphere)

    # Store the scraped data in a dictionary
    # Store data in a dictionary
    mars_data = {
        "news_title" : news_title,
        "paragraph_text": news_p,
        "featured_img_url" : featured_img_url,
        "mars_weather" : mars_weather,
        "mars_facts" : facts_table,
        "hemisphere_img_urls" : hemisphere_img_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
        
        