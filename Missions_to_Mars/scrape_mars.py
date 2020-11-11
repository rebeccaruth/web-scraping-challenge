import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape_main():
    executable_path = {"executable_path": "../chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = scrape_mars_news(browser)
    scrape_results = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": scrape_featured_img(browser),
        "mars_facts": scrape_mars_facts(browser),
        "hemispheres": scrape_hemispheres(browser)
    }
    browser.quit()
    return scrape_results


def scrape_mars_news(browser):
    #nasa url
    nasa_url = "https://mars.nasa.gov/news/"
    #open url in chrome
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, "html.parser")
    try: 
        #find first article on site
        first_article = soup.select_one("ul.item_list li.slide")
        #select title
        news_title = first_article.find("div", class_="content_title").get_text()
        #select paragraph
        news_p = first_article.find("div", class_="article_teaser_body").get_text()
    except: 
        return None, None 
    return news_title, news_p

def scrape_featured_img(browser):
    #image url
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #open url in chrome
    browser.visit(image_url)
    try:
        #find button
        fullimagebutton = browser.find_by_id("full_image")
        #click button
        fullimagebutton.click()
        #find next button and click
        more_info = browser.links.find_by_partial_text("more info")
        more_info.click()
        #find image 
        fullimage = soup.select_one("img", class_="main_image")
    except: 
        return None
    return fullimage

def scrape_mars_facts(browser):
    #mars facts url
    mars_url = "https://space-facts.com/mars/"
    #create table
    mars_facts = pd.read_html(mars_url)
    #create dataframe and set index
    mars_df = mars_facts[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    return mars_df.to_html(classes="table table-striped")

def scrape_hemispheres(browser):
    #mars hemisphere url
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #open url
    browser.visit(hemisphere_url)
    try:
      #create list for urls
        hemisphere_image_urls = []
        #create base url
        base_url= (hemisphere_url.split('/search'))[0]  
        links = browser.find_by_css("a.product-item h3")
        for l in range(len(links)):
            hemisphere = {}
            browser.find_by_css("a.product-item h3")[l].click()
            sample_link = browser.links.find_by_text('Sample').first
            hemisphere['url'] = sample_link['href']
            hemisphere['title'] = browser.find_by_css('h2.title').text
            hemisphere_image_urls.append(hemisphere)
            browser.back()
    except:
        return None
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_main())