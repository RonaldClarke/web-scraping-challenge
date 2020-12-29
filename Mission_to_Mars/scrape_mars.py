import requests
import json
from bs4 import BeautifulSoup as bs
import splinter
import pandas as pd
import pymongo


def scrape_info():
    executable_path = {'executable_path' : '/Users/ronaldclarke/Desktop/GitHub/web-scraping-challenge/Mission_to_Mars/chromedriver'}
    browser = splinter.Browser('chrome', **executable_path)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    content = soup.find('div', class_='content_page')
    titles = content.find_all('div', class_="content_title")
    headline = titles[0].text.strip()


    body = content.find_all('div', class_='article_teaser_body')
    para = body[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    browser.find_by_id('full_image').click()
    browser.find_by_text('more info     ').click()

    html = browser.html
    soup = bs(html, 'html.parser')
    feat_img = soup.find('img', class_='main_image')['src']

    im_url = f'https://www.jpl.nasa.gov{feat_img}'

    chart_url = 'https://space-facts.com/mars/'
    table = pd.read_html(chart_url)

    facts_df = table[0]
    facts_df.columns = ["Category", "Values"]
    mars_html = facts_df.to_html()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(hemisphere_url)

    hemi_html = browser.html
    hemisoup = bs(hemi_html, 'html.parser')

    item = hemisoup.find_all('div', class_='item')

    title = []
    url = []
    for i in item:
        title.append(i.find('h3').text.strip())
        url.append(base_url + i.find('a')['href'])  
    img_url = []
    for i in url:
        browser.visit(i)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = base_url + soup.find('img',class_='wide-image')['src']
        img_url.append(img)

    hemisphere_image_urls = []

    for i in range(len(title)):
        hemisphere_image_urls.append({'title':title[i],'img_url':img_url[i]})

    scrape_dict = {
    "headline" : headline,
    "para" : para,
    "im_url" : im_url,
    "mars_html" : mars_html,
    "hemisphere_image_urls" : hemisphere_image_urls
    }
    browser.quit()
    return scrape_dict

