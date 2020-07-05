from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# NASA Mars News
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(0.5)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")

    #  Parse Results HTML with BeautifulSoup
    try:
        slide_class = soup.select_one("ul.item_list li.slide")
        slide_class.find("div", class_="content_title")

    # Scrape the Latest News Title and Paragraph Text
        news_title = slide_class.find("div", class_="content_title").get_text()
        news_p = slide_class.find("div", class_="article_teaser_body").get_text()
    # Return results
    except AttributeError:
        return None, None
    return news_title, news_p

# JPL Mars Space Images 
def featured_image(browser):
    # Visit the url for JPL Featured Space Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(0.5)

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    featured_image = browser.find_by_id("full_image")
    featured_image.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = bs(html, 'lxml')

    featured_image_url = image_soup.select_one("figure.lede a img").get("src")

    # Use Base URL to Create Absolute URL
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"
    return featured_image_url

# Mars Weather
def twitter_weather(browser): 

    # Visit the Mars Weather twitter account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    # Parse Results HTML with BeautifulSoup
    html = browser.html
    mars_weather_soup = bs(html, "lxml")

    # Find a Tweet that shows `Mars Weather`
    mars_weather_tweets = mars_weather_soup.find_all("div", attrs={
                                                "data-testid": "tweet"
                                                    })

    weather_reports = []
    for tweet in mars_weather_tweets:
        for span in tweet.find_all('span'):    
            if "sol" in span.text:
                weather_reports.append(span.text)
                
    weather_results = weather_reports[0]                        
    print(weather_results)       
    return weather_results
            

# Mars Facts
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
        # Clean up DataFrame, set index
    df.columns=["Planet Profile", "Value"]
    df.set_index("Planet Profile", inplace=True)

    return df.to_html(classes="table table-striped")

# Mars Hemispheres
def hemispheres(browser):
    # Visit the USGS Astrogeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)    

    # Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name
    hemisphere_img_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[item].click()
    
        sample_img = browser.links.find_by_text("Sample").first
    
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere["img_url"] = sample_img["href"]     
    
        hemisphere_img_urls.append(hemisphere)
    
        browser.back()
    return hemisphere_img_urls

# Function to scrape Hemisphere
def scrape_hemishere(html_text):
    mars_weather_soup = bs(html_text, "lxml")
    try:
        title_tag = mars_weather_soup.find("h2", class_="title").get_text()
        sample_tag = mars_weather_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_tag = None
        sample_tag = None
    hemisphere = {
        "title": title_tag,
        "img_url": sample_tag
    }
    return hemisphere


# Scrape All
def scrape_all():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemispheres(browser)
    timestamp = dt.datetime.now()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }

    browser.quit()
    #return data
    return mars_data

if __name__ == "__main__":
    data = scrape_all()
    print(data)