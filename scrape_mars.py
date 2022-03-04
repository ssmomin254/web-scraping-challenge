import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import re
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)


    url = 'https://redplanetscience.com/'

    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')


    results = soup.find_all('div', class_='list_text')
    
    news = []
    # Loop through returned results
    for result in results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        news.append([news_title, news_p])

    for result in results:

    # Retrieve the thread title
        title = result.find('div', class_='content_title').text


    # Access the thread's text content
    title_text = result.find('div', class_='article_teaser_body').text

    try:
        print('\n-----------------\n')
        print(title)
        print(title_text)

    except AttributeError as e:
        print(e)


    # ## JPL Mars Space Images


    # url to scrape 
    url = 'https://spaceimages-mars.com/'


    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')



    featured_image= soup.find('img', class_='headerimage fade-in')
    #featured_image= url + image url
    featured_image


    featured_url = featured_image['src']
    featured_url



    #featured image url cat
    featured_image_df = pd.Series([url,featured_url])
    full_url = featured_image_df.str.cat()
    full_url


    # ## Mars Facts


    url = 'https://galaxyfacts-mars.com'



    tables = pd.read_html(url)
    df = tables[0]
    df.head()



    #grab column heads

    df.columns = df.iloc[0] 
    df.drop(index=df.index[0], 
    axis=0, 
    inplace=True)
    df




    #set new index
    df.set_index('Mars - Earth Comparison')




    #to html
    facts_html = df.to_html()
    facts_html



    #clean up
    facts_html.replace('\n','')



    #export html file
    df.to_html('facts.html')


    print(facts_html)


    # ## Mars Hemispheres


    # Setup splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://marshemispheres.com/'



    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')



    results = soup.find_all('div', class_='description')


    titles = []
    for result in results:
        title = result.find('h3').text
        titles.append(title)
        
    #Retrieve just the first word of the title
    first_titles = []

    for title in titles: 
        first_title = title.split()[0]
        first_titles.append(first_title)
  
    #Put the first word of the title in lowercase.
    for i in range(len(first_titles)):
        first_titles[i] = first_titles[i].lower()

    images_url = []

    for title in first_titles:
    #Writing out the full url of the featured image.
        url_df = pd.Series([url,title,'.html'])

        image_url = url_df.str.cat()
        browser.visit(image_url)
    
        html = browser.html
        soup = bs(html, 'html.parser')

        full_image_url = soup.find('img', class_ = 'wide-image')['src']
        image_url_df = pd.Series([url,full_image_url])
        final_image_url = image_url_df.str.cat()
        images_url.append(final_image_url)

    hemisphere_image_urls = []
    for x in range(0,4):
        hemisphere_dict = {'title': titles[x], 'images_url': images_url[x]}
        hemisphere_image_urls.append(hemisphere_dict)



    # Assigning scraped data to a page
    marspage = {
    "news_title" : news_title,
    "news_p" : news_p,
    "featured_image_url" : full_url ,#look for full object
    "facts_html": facts_html,
    "hemisphere_image_urls" : hemisphere_image_urls
    }
    return marspage