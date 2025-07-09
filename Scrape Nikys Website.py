#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install required packages for web scraping
get_ipython().run_line_magic('pip', 'install requests beautifulsoup4 selenium pandas lxml')


# In[3]:


# Import required libraries for web scraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Firefox options for headless browsing
firefox_options = Options()
firefox_options.add_argument("--headless")

# Initialize the webdriver
driver = webdriver.Firefox(options=firefox_options)

print("Starting to scrape the website...")

# Navigate to the URL
url = "https://www.nikys-sports.com/collections/turf?page=1"
driver.get(url)

# Wait for the page to load
time.sleep(5)

print("Page loaded successfully")


# In[5]:


# Let's try using requests and BeautifulSoup first to see if we can scrape the content
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Try to get the page content with requests first
url = "https://www.nikys-sports.com/collections/turf?page=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Attempting to scrape with requests...")
response = requests.get(url, headers=headers)
print("Status code:", response.status_code)
print("Content length:", len(response.content))

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
print("Successfully parsed HTML content")


# In[6]:


# Let's examine the page structure to find product information
# Look for product containers, cards, or similar elements

# Find all potential product containers
product_containers = soup.find_all('div', class_=lambda x: x and ('product' in x.lower() or 'item' in x.lower() or 'card' in x.lower()))
print("Found", len(product_containers), "potential product containers")

# Let's also look for common e-commerce patterns
grid_containers = soup.find_all('div', class_=lambda x: x and ('grid' in x.lower() or 'collection' in x.lower()))
print("Found", len(grid_containers), "grid/collection containers")

# Look for any tables
tables = soup.find_all('table')
print("Found", len(tables), "tables")

# Let's examine the page title and some key elements
title = soup.find('title')
if title:
    print("Page title:", title.get_text().strip())

# Look for product links or anchors
product_links = soup.find_all('a', href=lambda x: x and '/products/' in x)
print("Found", len(product_links), "product links")


# In[7]:


# Let's look for specific product information patterns
# First, let's examine the structure more carefully

# Look for product cards or items with more specific selectors
product_cards = soup.find_all('div', class_=lambda x: x and any(keyword in x.lower() for keyword in ['product-card', 'product-item', 'item-card', 'card-product']))
print("Product cards found:", len(product_cards))

# Look for price elements
prices = soup.find_all(class_=lambda x: x and 'price' in x.lower())
print("Price elements found:", len(prices))

# Look for product titles/names
titles = soup.find_all(class_=lambda x: x and any(keyword in x.lower() for keyword in ['title', 'name', 'product-title']))
print("Title elements found:", len(titles))

# Let's examine the actual HTML structure by looking at some key divs
main_content = soup.find('main') or soup.find('div', {'id': 'main'}) or soup.find('div', class_=lambda x: x and 'main' in x.lower())
if main_content:
    print("Found main content area")
    # Look for collection or product grid within main content
    collection_grid = main_content.find('div', class_=lambda x: x and any(keyword in x.lower() for keyword in ['collection', 'grid', 'products']))
    if collection_grid:
        print("Found collection grid within main content")
        print("Grid classes:", collection_grid.get('class', []))
    else:
        print("No collection grid found in main content")


# In[19]:


# Let's try a different approach - look for JSON data or script tags that might contain product information
import json
import re

# Look for script tags that might contain product data
scripts = soup.find_all('script')
print("Found", len(scripts), "script tags")

# Look for JSON-LD structured data
json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
print("Found", len(json_ld_scripts), "JSON-LD scripts")

# Look for scripts containing product data
product_data_scripts = []
for script in scripts:
    if script.string and any(keyword in script.string.lower() for keyword in ['product', 'collection', 'items', 'variants']):
        product_data_scripts.append(script)

print("Found", len(product_data_scripts), "scripts potentially containing product data")

# Let's also try to find the actual product elements by looking at the page structure
# Sometimes products are in article tags or specific div structures
articles = soup.find_all('article')
print("Found", len(articles), "article tags")

# Look for any elements with data attributes that might contain product info
elements_with_data = soup.find_all(attrs=lambda x: x and any(key.startswith('data-') for key in x.keys()))
print("Found", len(elements_with_data), "elements with data attributes")


# In[ ]:


# Fix the attribute search and look for data attributes more carefully
# Let's examine the JSON-LD scripts first since we found 4 of them
json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})

print("Examining JSON-LD scripts:")
for i, script in enumerate(json_ld_scripts):
    if script.string:
        try:
            data = json.loads(script.string)
            print("Script", i + 1, "contains:", type(data))
            if isinstance(data, dict):
                print("Keys:", list(data.keys())[:5])  # Show first 5 keys
            elif isinstance(data, list) and len(data) > 0:
                print("List with", len(data), "items")
                if isinstance(data[0], dict):
                    print("First item keys:", list(data[0].keys())[:5])
        except json.JSONDecodeError:
            print("Script", i + 1, "contains invalid JSON")

# Let's also look for elements with specific data attributes
elements_with_product_data = soup.find_all(attrs={'data-product-id': True})
print("Elements with data-product-id:", len(elements_with_product_data))

elements_with_variant_data = soup.find_all(attrs={'data-variant-id': True})
print("Elements with data-variant-id:", len(elements_with_variant_data))


# In[ ]:


# Let's examine the JSON-LD scripts in detail to see if they contain product data
json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})

for i, script in enumerate(json_ld_scripts):
    if script.string:
        try:
            data = json.loads(script.string)
            print("=== JSON-LD Script", i + 1, "===")
            
            if isinstance(data, dict):
                # Check if this contains product information
                if data.get('@type') == 'Product':
                    print("Found Product schema!")
                    print("Product data:", data)
                elif data.get('@type') == 'BreadcrumbList':
                    print("Breadcrumb navigation data")
                    if 'itemListElement' in data:
                        print("Breadcrumb items:", len(data['itemListElement']))
                elif data.get('@type') == 'Organization':
                    print("Organization data")
                else:
                    print("Type:", data.get('@type'))
                    print("Keys:", list(data.keys()))
                    # Print first few key-value pairs
                    for key in list(data.keys())[:3]:
                        print(key + ":", str(data[key])[:100])
            print()
        except json.JSONDecodeError as e:
            print("Script", i + 1, "JSON decode error:", e)
            print()


# In[12]:


# Let's examine the ItemList JSON-LD script in detail - this likely contains our product data
json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})

# Get the ItemList script (script 3)
itemlist_script = json_ld_scripts[2]  # 0-indexed, so script 3 is index 2
data = json.loads(itemlist_script.string)

print("ItemList contains", len(data['itemListElement']), "products")
print()

# Let's examine the first few products
for i, item in enumerate(data['itemListElement'][:3]):
    print("=== Product", i + 1, "===")
    for key, value in item.items():
        print(key + ":", value)
    print()

# Let's also see what keys are available in all products
all_keys = set()
for item in data['itemListElement']:
    all_keys.update(item.keys())

print("Available keys across all products:", sorted(all_keys))


# In[14]:


# Extract all product data from the JSON-LD ItemList
import pandas as pd

json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
itemlist_script = json_ld_scripts[2]
data = json.loads(itemlist_script.string)

# Create a list to store product information
products = []

for item in data['itemListElement']:
    product = {
        'position': item.get('position'),
        'name': item.get('name'),
        'url': item.get('url')
    }
    products.append(product)

# Create DataFrame
df = pd.DataFrame(products)

print("Successfully extracted", len(products), "products from the turf category")
print()
print("Sample of the data:")
print(df.head(10))

# Save to CSV file
df.to_csv('nikys_sports_turf_products.csv', index=False)
print()
print("Data saved to nikys_sports_turf_products.csv")
print("Full dataset shape:", df.shape)


# In[16]:


# Extract all product data from the JSON-LD ItemList
import pandas as pd

json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
itemlist_script = json_ld_scripts[2]
data = json.loads(itemlist_script.string)

# Create a list to store product information
products = []

for item in data['itemListElement']:
    product = {
        'position': item.get('position'),
        'name': item.get('name'),
        'url': item.get('url')
    }
    products.append(product)

# Create DataFrame
df = pd.DataFrame(products)

print("Successfully extracted", len(products), "products from the turf category")
print()
print("Sample of the data:")
print(df.head(10))

# Save to CSV file
df.to_csv('nikys_sports_turf_products.csv', index=False)
print()
print("Data saved to nikys_sports_turf_products.csv")
print("Full dataset shape:", df.shape)


# In[ ]:





# In[ ]:




