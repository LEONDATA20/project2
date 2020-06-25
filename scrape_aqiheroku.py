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

    # ufo_url='http://127.0.0.1:5500/flask/templates/ufo.html'  #golive url
    # ufo_soup = scrape_url(ufo_url)
    # ufo_table = str(ufo_soup.find('tbody'))
    # weather_data['ufo'] = ufo_table


    # #how we get the data
    # countries_df = pd.read_html('https://developers.google.com/public-data/docs/canonical/countries_csv')
    # clean_countries = countries_df[0].rename(columns={"name":"Country","country":"Abbr"})
    # lat = clean_countries['latitude']
    # lon = clean_countries['longitude']
    # md = zip(lat,lon)
    # ri = list(md)
    # saving_to_list = []
    # for x in ri:
    #     lat_lng = f'https://api.airvisual.com/v2/nearest_city?lat={round(list(x)[0],2)}&lon={round(list(x)[1],2)}&key={API_KEY}' 
    #     time.sleep(12)# reach 'https://www.iqair.com/air-pollution-data-api/plans'
    #     lat_lng_response = requests.get(lat_lng).json()
    #     try:
    #         saving_to_list.append(lat_lng_response)
    #         pprint(lat_lng_response)
    #     except:
    #         print("Something went wrong")
    #     pass
    # import json
    # with open('data.json', 'w') as f:
    #     json.dump(final_list, f)


    weather_data['nm'] = 'test'

    return weather_data






    # # Featured Image
    # url_img='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # img_soup = scrape_url(url_img)
    # img_url = img_soup.find('div',class_='img').find('img')['src']
    # featured_image_url = f'https://www.jpl.nasa.gov{img_url}'

    # weather_data['featured_image_url'] = featured_image_url


    # # Mars Weather
    # url_weather='https://twitter.com/marswxreport?lang=en'
    # weather_soup = scrape_url(url_weather)
    # mars_weather = weather_soup.find('div',lang='en').find('span').text

    # weather_data['mars_weather'] = mars_weather


    # # Mars Facts
    # url_table='https://space-facts.com/mars/'
    # table_soup = scrape_url(url_table)
    # mars_table = str(table_soup.find('tbody'))
    
    # weather_data['mars_facts'] = mars_table

    # # tables = pd.read_html(url_table)
    # # df = tables[0]
    # # df.columns=['parameter','value']
    # # html_table = df.to_html()
    # # facts_table = html_table.replace('\n', ' ')
    # #df.to_html('table.html')
    # #mars_data['table'] = facts_table
    

    # # Mars Hemispheres
    # url_mars='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # mars_soup = scrape_url(url_mars)
    # items = mars_soup.find_all('div', class_='description')

    # hemisphere_image_urls=[]
    # for item in items:
    #     title=item.h3.text
    #     url=item.find('a')['href']
    #     z={'title':title,'img_url':f'https://astrogeology.usgs.gov{url}'}
    #     hemisphere_image_urls.append(z)
    
    # md=[]
    # for i_url in hemisphere_image_urls:
    #     image_soup = scrape_url(i_url['img_url'])
    #     x= image_soup.find('ul').find('a')['href']
    #     y={'title':i_url['title'],'img_url':x}
    #     md.append(y)


    # weather_data['title_url'] = md
    

    

# scrape()










    




















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