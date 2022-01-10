# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
	# set executable path
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=True)
	
	news_title, news_paragraph = mars_news(browser)
	hemi_titles = hemisphere_data(browser)

	# Run all scraping functions and store results in dictionary
	data = {
		"news_title": news_title,
		"news_paragraph": news_paragraph,
		"featured_image": featured_image(browser),
		"facts": mars_facts(),
		"last_modified": dt.datetime.now(),
		"hemisphere_images": hemi_titles
	}

	# Stop webdriver and return data
	browser.quit()
	return data

def mars_news(browser):
    
	# assign the url and instruct the browser to visit it
	# Visit the mars nasa news site
	url = 'https://redplanetscience.com'
	browser.visit(url)

	# Optional delay for loading the page
	browser.is_element_present_by_css('div.list_text', wait_time=1)

	# set up the HTML parser
	html = browser.html
	news_soup = soup(html, 'html.parser')

	try:
		slide_elem = news_soup.select_one('div.list_text')
		# looking for a <div /> with a class of “content_title"
		#slide_elem.find('div', class_='content_title')

		# Clear HTML in our output
		# Use the parent element to find the first `a` tag and save it as `news_title`
		news_title = slide_elem.find('div', class_='content_title').get_text()

		# Use the parent element to find the paragraph text
		news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

	except AttributeError:
		return None, None

	return news_title, news_p

# Featured Images
# automate all of the clicks

def featured_image(browser):

	# Visit URL
	url = 'https://spaceimages-mars.com'
	browser.visit(url)

	# Find and click the full image button
	full_image_elem = browser.find_by_tag('button')[1]
	full_image_elem.click()

	# Parse the resulting html with soup
	html = browser.html
	img_soup = soup(html, 'html.parser')

	try:
		# Find the relative image url
		img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
	except AttributeError:
		return None

	# Use the base URL to create an absolute URL
	img_url = f'https://spaceimages-mars.com/{img_url_rel}'

	return img_url

def mars_facts():
	try:
		# Scrape tables with Pandas
		# Mars Facts
		df = pd.read_html('https://galaxyfacts-mars.com')[0]
	except BaseException:
		return None

	# Assign columns and set index of dataframe
	df.columns=['description', 'Mars', 'Earth']
	df.set_index('description', inplace=True)

	# Pandas: convert DataFrame back into HTML-ready code using the .to_html() function
	return df.to_html()

def  hemisphere_data(browser):
	# 1. Use browser to visit the URL 
	url = 'https://marshemispheres.com/'
	browser.visit(url)

	# 2. Create a list to hold the images and titles.
	hemisphere_image_urls = []
	
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
	# scraped data as a list of dictionaries
	# URL string and title of each hemisphere image
	return hemisphere_image_urls

	# 5. Quit the browser
	browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())	