
# Mission To Mars


```python
# Import Dependencies
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
```


```python
# URL of the page to be scraped
url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')
```

### NASA Mars News


```python
# Retrieve the latest News Title and Paragraph Text
news_title = soup.find('div', class_='content_title').text.strip()

news_p = soup.find('div', class_='rollover_description_inner').text

print("News Title: ", news_title)

print("Paragraph Text: ", news_p)
```

    News Title:  NASA Garners 7 Webby Award Nominations
    Paragraph Text:  
    Nominees include four JPL projects: the solar system and climate websites, InSight social media, and a 360-degree Earth video. Public voting closes April 18, 2019.
    


### JPL Mars Space Images - Featured Image


```python
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = bs(html, 'html.parser')

base_url = 'https://www.jpl.nasa.gov'

img_url = soup.find("a", {"class":"button fancybox"})['data-fancybox-href']

featured_img_url = base_url + img_url
print("Featured Image URL: ", featured_img_url)
```

    Featured Image URL:  https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19674_ip.jpg


### Mars Weather


```python
# URL of the page to be scraped
url = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')

# Retrieve the parent HTML tag
li_tags = soup.findAll('li', class_='js-stream-item stream-item stream-item')

div_content = li_tags[0].find('div', class_='content')
div_tweet = div_content.find('div', class_='js-tweet-text-container')
mars_weather = div_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

print("Mars Weather: ", mars_weather)
```

    Mars Weather:  InSight sol 131 (2019-04-09) low -98.2ºC (-144.8ºF) high -15.6ºC (3.8ºF)
    winds from the WNW at 4.1 m/s (9.1 mph) gusting to 11.6 m/s (26.0 mph)
    pressure at 7.30 hPapic.twitter.com/g5upn7bkE5


### Mars Facts


```python
# URL of the page to be scraped
url = 'http://space-facts.com/mars/'

# Scrape the table containing facts about Mars
tables = pd.read_html(url , encoding= "utf-8")
tables
```




    [                      0                              1
     0  Equatorial Diameter:                       6,792 km
     1       Polar Diameter:                       6,752 km
     2                 Mass:  6.42 x 10^23 kg (10.7% Earth)
     3                Moons:            2 (Phobos & Deimos)
     4       Orbit Distance:       227,943,824 km (1.52 AU)
     5         Orbit Period:           687 days (1.9 years)
     6  Surface Temperature:                  -153 to 20 °C
     7         First Record:              2nd millennium BC
     8          Recorded By:           Egyptian astronomers]




```python
# Create a dataframe from the table
df = tables[0]
df = df.T
df = df.iloc[1:]
df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
              'Orbital Distance', 'Orbital Period', 'Surface Temperature', 
              'First Record', 'Recorded By']
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Equatorial Diameter</th>
      <th>Polar Diameter</th>
      <th>Mass</th>
      <th>Moons</th>
      <th>Orbital Distance</th>
      <th>Orbital Period</th>
      <th>Surface Temperature</th>
      <th>First Record</th>
      <th>Recorded By</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>6,792 km</td>
      <td>6,752 km</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
      <td>2 (Phobos &amp; Deimos)</td>
      <td>227,943,824 km (1.52 AU)</td>
      <td>687 days (1.9 years)</td>
      <td>-153 to 20 °C</td>
      <td>2nd millennium BC</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Convert pandas dataframe to HTML table string
html_table = df.to_html()
html_table.replace('\n', '')
html_table
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Equatorial Diameter</th>\n      <th>Polar Diameter</th>\n      <th>Mass</th>\n      <th>Moons</th>\n      <th>Orbital Distance</th>\n      <th>Orbital Period</th>\n      <th>Surface Temperature</th>\n      <th>First Record</th>\n      <th>Recorded By</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>1</th>\n      <td>6,792 km</td>\n      <td>6,752 km</td>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n      <td>227,943,824 km (1.52 AU)</td>\n      <td>687 days (1.9 years)</td>\n      <td>-153 to 20 °C</td>\n      <td>2nd millennium BC</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'



### Mars Hemispheres


```python
# URL of the page to be scraped
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')

# Retrieve the parent tag containing all hemispheres
links = []       # List to store the links to be visited
hemisphere_img_urls = []    # List to store the dictionaries for each hemisphere

base_url = "https://astrogeology.usgs.gov"

div_result = soup.find('div', class_='result-list')
div_items = div_result.findAll('div', class_='item')

for div_item in div_items:
    hemisphere = {}
    div_content = div_item.find('div', class_='description')
    
    title = div_content.find('h3').text
    hemisphere['title'] = title
    
    href = div_item.find('a', {"class":"itemLink product-item"})['href']
    links.append(base_url + href)

    for link in links:
        response = requests.get(link)
        soup = bs(response.text, 'lxml')

        img_src = soup.find("img", {"class":"wide-image"})['src']
        img_url = base_url + img_src
        hemisphere['img_url'] = img_url
        
    hemisphere_img_urls.append(hemisphere)
        
for item in hemisphere_img_urls:
    print(item)
```

    {'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}
    {'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}
    {'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}
    {'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}

