#!/usr/bin/env python
# coding: utf-8

# In[75]:

def scrape():
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import requests
    import re
    import nbconvert
    import time


    # In[76]:


    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


    #Retrieve page with requests

    response = requests.get(url)

    # Parse the response with beautifulsoup

    soup = bs(response.text, 'html.parser')


    # Pretty Print the html
    #print(soup.prettify())


    # In[77]:


    #Store and Print the news title

    news_title = soup.find('div',class_='content_title').text

    #print(news_title)


    # In[78]:


    # Navigate and Parse the article URL

    p_url = "https://mars.nasa.gov/news/8719/nasa-invites-public-to-share-excitement-of-mars-2020-perseverance-rover-launch/"

    response = requests.get(p_url)

    soup = bs(response.text,'lxml')


    # In[79]:


    # Store the first paragraph in news_p

    results = soup.find_all('p')

    paragraphs = []

    for result in results:
        paragraphs.append(result)

    news_p = paragraphs[2].text
        
    #print(news_p)




    # In[80]:


    # Activate splinter
    executable_path = {'executable_path': r'C:\Users\nvora\AppData\Roaming\chromedriver_win32\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[35]:


    # Open URL in splinter
    splinter_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(splinter_url)


    # In[36]:


    # Click Full Image link
    browser.click_link_by_id('full_image')


    # In[37]:


    # Navigate to more info to find the full size image

    browser.click_link_by_partial_text('more info')


    # In[38]:


    # Extract the full-size image url

    featured_image_url = browser.find_by_css('.main_image')[0]['src']

    browser.quit()


    # In[60]:


    # Connect Browser to Twitter URL (Splinter)

    executable_path = {'executable_path': r'C:\Users\nvora\AppData\Roaming\chromedriver_win32\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    twitter_url = 'https://twitter.com/MarsWxReport'

    browser.visit(twitter_url)
    time.sleep(5)

    # In[61]:


    # Scrape Mars HTML

    html = browser.html

    soup = bs(html,'html.parser')

    #print(soup.prettify())


    # In[63]:


    #Scrape Mars Tweet text and store in variable

    mars_weather = soup.find_all('span',class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[27].text
    browser.quit()


    # In[1]:


    # Pandas Scraping Mars Facts

    url = 'https://space-facts.com/mars/'


    # In[7]:


    # Needed to run conda install -c conda-forge html5lib on the PythonData kernel to get this working
    # Read URL HTML into tables

    tables = pd.read_html(url)
    tables[0]


    # In[ ]:


    mars_facts = tables[0].to_html()


    # In[65]:


    # Splinter scrape image urls
    executable_path = {'executable_path': r'C:\Users\nvora\AppData\Roaming\chromedriver_win32\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    mars_images_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_images_url)


    # In[67]:


    # Click first link URL and store image URL and title

    browser.find_by_css('h3')[0].click()
    cerberus_image = browser.find_by_text('Sample')['href']
    cerberus_title = browser.find_by_css('.title').text

    #Return to main page

    browser.back()


    # In[68]:


    # Click second link URL and store image URL and title

    browser.find_by_css('h3')[1].click()
    schiaparelli_image = browser.find_by_text('Sample')['href']
    schiaparelli_title = browser.find_by_css('.title').text

    browser.back()


    # In[69]:


    # Click second link URL and store image URL and title

    browser.find_by_css('h3')[2].click()
    syrtis_major_image = browser.find_by_text('Sample')['href']
    syrtis_major_title = browser.find_by_css('.title').text

    browser.back()


    # In[70]:


    # Click second link URL and store image URL and title

    browser.find_by_css('h3')[3].click()
    valles_marineris_image = browser.find_by_text('Sample')['href']
    valles_marineris_title = browser.find_by_css('.title').text

    browser.quit()


    # In[71]:


    # Append the images to a dictionary

    hemisphere_images = [
        {"title": cerberus_title, "img_url": cerberus_image},
        {"title": schiaparelli_title, "img_url": schiaparelli_image},
        {"title": syrtis_major_title, "img_url": syrtis_major_image},
        {"title": valles_marineris_title, "img_url": valles_marineris_image}
    ]

    # print(hemisphere_images)    
    
    mars_dict = {'mars_news':news_title,'news_summary':news_p,'featured_mars_image':featured_image_url,'mars_weather':mars_weather,'mars_facts':mars_facts,'mars_hemispheres':hemisphere_images}
    return mars_dict
