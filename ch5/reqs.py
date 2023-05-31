"""
Author: Aleksa Zatezalo
Date: May 22th 2023
Description: Making requests in python.
"""

import urllib.parse
import urllib.request
import requests
from lxml import etree
from io import BytesIO
from bs4 import BeautifulSoup as bs

# GET 
url = 'http://google.com'
with urllib.request.urlopen(url) as response: # GET
    content = response.read()

print(content)

# Using xtree to Parse URL Requests
r = requests.get(url) # GET
content = r.content # content is of type 'bytes'
parser  = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser) # parse into a tree
for link in content.findall('//a'): # find all "a" anchor elements
    print(f"{link.get('href')} -> {link.text}")

# using BS to parse html record - Code below suffers from an install error
# tree = bs(r.text, 'html.parse') # Parse into tree
# for link in tree.find_all('a'): # find all "a" anchor elements.
#     print(f"{link.get('href')} -> {link.text}") 