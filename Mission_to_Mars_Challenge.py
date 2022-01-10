# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# assign the url and instruct the browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# looking for a <div /> with a class of “content_title"
slide_elem.find('div', class_='content_title')

# Clear HTML in our output
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# automate all of the clicks
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts: Scrape tables with Pandas

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Pandas: convert DataFrame back into HTML-ready code using the .to_html() function
df.to_html()

# End the automated browsing session
browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# Empty dictionary
#hemispheres = {}

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    # Empty dictionary
    hemispheres = {}
    
    # using tags
    # Find and click the full image button
    full_image = browser.find_by_tag('h3')[i]
    full_image.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Find the relative image url
    img_url = img_soup.find('img', class_='thumb')['src']
    
    # Find `title`
    title = img_soup.find('h2', class_='title').text
    
    # Add images and title
    hemisphere_image_urls.append({'title': title, 'img_url': f'https://marshemispheres.com/{img_url}'})
    hemisphere_image_urls.append(hemispheres)
    
    # use browser.back() to navigate back to the beginning to get the next hemisphere image
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

