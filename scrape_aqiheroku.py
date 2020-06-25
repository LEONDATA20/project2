# from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import numpy as np



def scrape_url (url):
    response = requests.get(url) 
    soup =  bs(response.text, "html.parser")
    # browser.quit()
    return soup


def scrape():
    # create data dict that we can insert into mongo
    weather_data = {}

    # # table 
    url_tables = 'https://www.iqair.com/world-air-quality'
    test_soup = scrape_url(url_tables)
    table = test_soup.find('div', class_='ranking')

    country_url = []
    tests = table.find_all('div',class_ = 'name')
    for test in tests:
        wocao = test.find('a')['href']
        country_url.append(f'https://www.iqair.com{wocao}')

    # number:
    number_list = table.find_all('div',class_ = 'aqi-number')
    nmd=[]
    for x in number_list:
        number=x.text
        nmd.append(int(number))
    
    country_name=[]
    for test in tests:
        ri = test.find('a').text
        country_name.append(ri)
    
    index = [1,2,3,4,5,6,7,8,9,10]

    td_list = list(zip(index, country_url, country_name, nmd))

    weather_data['td'] = td_list


    # Summary from WHO
    who_url='https://www.who.int/news-room/q-a-detail/q-a-on-climate-change-and-covid-19#'
    summary_soup = scrape_url(who_url)  # question2
    answer1 = summary_soup.find_all('div',class_ = 'sf-accordion__content')[1].find_all('p')[1].text
    answer2 = summary_soup.find_all('div',class_ = 'sf-accordion__content')[3].find_all('p')[2].text
    weather_data['q1'] = answer1
    weather_data['q2'] = answer2


    weather_data['nm'] = 'test'

    return weather_data







   
    










    




















##

#     url_news='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
#     ##browser.visit(url_news)
#     ##time.sleep(1)
#     ##html = browser.html
#     ##soup = bs(html, "html.parser")

#     # Scrape page into Soup
#     html = browser.html
#     soup = bs(html, "html.parser")

#     # Get the average temps
#     avg_temps = soup.find('div', id='weather')

#     # Get the min avg temp
#     min_temp = avg_temps.find_all('strong')[0].text

#     # Get the max avg temp
#     max_temp = avg_temps.find_all('strong')[1].text

#     # BONUS: Find the src for the sloth image
#     relative_image_path = soup.find_all('img')[2]["src"]
#     sloth_img = url + relative_image_path

#     # Store data in a dictionary
#     costa_data = {
#         "sloth_img": sloth_img,
#         "min_temp": min_temp,
#         "max_temp": max_temp
#     }

#     # Close the browser after scraping
#     browser.quit()

#     # Return results
#     return costa_data
# ##