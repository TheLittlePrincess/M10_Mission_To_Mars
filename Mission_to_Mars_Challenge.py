#!/usr/bin/env python
# coding: utf-8

# ### COPYING AND PASTING CHALLENGE STARTER CODE AS INSTRUCTED

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ## Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[12]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[13]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image

# In[14]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[15]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[16]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
#img_soup


# In[17]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[18]:


# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ## Mars Facts

# In[19]:


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()


# In[20]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[21]:


df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[22]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)


# In[23]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and image titles for each hemisphere.
for x in range(4):
    hemispheres = {}
    hemisphere_link = browser.find_by_tag('h3')[x]
    hemisphere_link.click()
    
    # Parse the HTML
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Find the relative image URL and title
    img_url_rel = browser.find_by_text('Sample').first
    hemispheres['img_url'] = img_url_rel['href']
    title = img_soup.find('h2').get_text()
    
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html/{img_url_rel}'

    # Add image URL and title to hemisphere_image_urls list
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Go back and click on the next image
    browser.back()


# In[24]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse HTML with soup
html_hemispheres = browser.html
hemisphere_soup = soup(html_hemispheres, 'html.parser')
hemispheres = hemisphere_soup.find_all('div', class_='item')

hemispheres_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'

# Loop through hemisphere info
for x in hemispheres:
    
    #title
    title = x.find('h3').text
    
    end_img_url = x.find('a', class_='itemLink product-item')['href']
    
    browser.visit(hemispheres_url + end_img_url)

    img_html = browser.html
    img_soup = soup(img_html, 'html.parser')
    img_url = hemispheres_url +img_soup.find('img', class_='wide-image')['src']
    
    hemisphere_image_urls.append({'img_url' : img_url, 'title' : title})    


# In[55]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[25]:


# 5. Quit the browser
browser.quit()


# In[ ]:




