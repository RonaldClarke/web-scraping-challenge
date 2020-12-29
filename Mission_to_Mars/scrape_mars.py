#!/usr/bin/env python
# coding: utf-8

# In[129]:


import requests
import json
from bs4 import BeautifulSoup as bs
import splinter
import pandas as pd
import pymongo


# In[130]:

def scrape():
    executable_path = {'executable_path' : '/Users/ronaldclarke/Desktop/GitHub/web-scraping-challenge/Mission_to_Mars/chromedriver'}
    browser = splinter.Browser('chrome', **executable_path)


# In[131]:


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html


# In[132]:


    soup = bs(html, 'html.parser')
    


# In[137]:


    content = soup.find('div', class_='content_page')


# In[138]:


    titles = content.find_all('div', class_="content_title")
    print(titles[0].text.strip())


# In[139]:


    headline = titles[0].text.strip()



# In[140]:


    body = content.find_all('div', class_='article_teaser_body')
    body = body[0].text



# In[52]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html


# In[53]:


    browser.find_by_id('full_image').click()


# In[54]:


    browser.find_by_text('more info     ').click()


# In[55]:


    html = browser.html
    soup = bs(html, 'html.parser')
    feat_img = soup.find('img', class_='main_image')['src']


# In[56]:


    im_url = f'https://www.jpl.nasa.gov{feat_img}'


    chart_url = 'https://space-facts.com/mars/'
    table = pd.read_html(chart_url)
    table


# In[66]:


    facts_df = table[0]
    facts_df.columns = ["Category", "Values"]



# In[68]:


    mars_html = facts_df.to_html()



# In[81]:


    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(hemisphere_url)


# In[70]:


    hemi_html = browser.html
    hemisoup = bs(hemi_html, 'html.parser')


# In[80]:


    item = hemisoup.find_all('div', class_='item')


# In[87]:


    title = []
    url = []
    for i in item:
        title.append(i.find('h3').text.strip())
        url.append(base_url + i.find('a')['href'])  
   



# In[88]:


    img_url = []
    for i in url:
        browser.visit(i)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = base_url + soup.find('img',class_='wide-image')['src']
        img_url.append(img)



# In[91]:


    hemisphere_image_urls = []

    for i in range(len(title)):
        hemisphere_image_urls.append({'title':title[i],'img_url':img_url[i]})

    mars_data = {}
    mars_data["headline"] = headline
    mars_data["paragraph"] = body
    mars_data["featured_image"] = im_url
    mars_data["mars_facts"] = mars_html
    mars_data["hemispheres"] = hemisphere_image_urls



