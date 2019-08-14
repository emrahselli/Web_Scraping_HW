import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

executable_path = {'executable_path': 'assets/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape ():
    mars_data = {}
    # Scraping Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")
    news = news_soup.find("div", class_='list_text')
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_ ="article_teaser_body").text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    #Scraping Mars Featured Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, "html.parser")
    image = image_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image
    mars_data["featured_image_url"] = featured_image_url

    #Scraping  Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    tweets = weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    mars_data["mars_weather"] = mars_weather

    #Scraping Mars Facts
    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)
    facts_df = table[1]
    facts_df.columns = ["Parameter", "Values"]
    facts_html = facts_df.to_html(header = False, index = False)
    mars_data["facts"] = facts_html

    #Scraping Mars Hemisphere Images
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls = []

    for i in range(1,9,2):
        hemisphere = {}
        
        browser.visit(hemisphere_url)
        hemisphere_html = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
        name_links = hemisphere_soup.find_all('a', class_='product-item')
        hemi_name = name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        browser.find_link_by_text('Sample').first.click()
        browser.windows.current = browser.windows[-1]
        hemisphere_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
        hemi_url = hemisphere_soup.find('img')['src']

        hemisphere['title'] = hemi_name.strip()
        hemisphere['img_url'] = hemi_url

        hemisphere_image_urls.append(hemisphere)

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_data