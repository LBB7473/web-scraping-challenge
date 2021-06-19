from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    headline, bodytext = news(browser)

    data = {
        "headline": headline,
        "bodytext": bodytext,
        "image_url": displayImage(browser),
        "mars_earth": marsEarth(),
        "hemispheres": hemiSpheres(browser)
    }

    browser.quit()
    
    return data

def news(browser):
    
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    headline = soup.select_one('div.list_text').find('div', class_='content_title').get_text()
    bodytext = soup.select_one('div.list_text').find('div', class_='article_teaser_body').get_text()

    return headline, bodytext

def displayImage(browser):
    
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_="headerimage").get('src')
    image_url = f'https://spaceimages-mars.com/{image}'

    return image_url

def marsEarth():

    mars_earth = pd.read_html('https://galaxyfacts-mars.com')[0]
    mars_earth.columns=['Description', 'Mars', 'Earth']
    mars_earth.set_index('Description', inplace=True)
    
    return mars_earth.to_html(classes="table table-striped")

def hemiSpheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    items = browser.find_by_css('a.product-item img')
    hemisphere_image_urls = []
    for i in range(len(items)):
        hem_url = {}
        browser.find_by_css('a.product-item img')[i].click()
        img_link = browser.links.find_by_text('Sample').first
        hem_url['title'] = browser.find_by_css('h2.title').text
        hem_url['img_url'] = img_link['href']
        hemisphere_image_urls.append(hem_url)
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":

    print(scrape_all())