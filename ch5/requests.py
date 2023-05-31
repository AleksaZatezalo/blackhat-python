"""
Author: Aleksa Zatezalo
Date: May 22th 2023
Description: Making requests in python.
"""

import urllib.parse
import urllib.request

# GET Resuests
# url = 'http://google.com'
# with urllib.request.urlopen(url) as response: # GET
#     content = response.read()

# print(content)

# POST Requests
# info = {'user:', 'tim', 'passwd:', '31337'}
# data = urllib.parse.urlencode(info).encode() # data is now of type bytes

# req = urllib.request.Request(url, data)
# with urllib.request.urlopen(req) as response: # POST
#     content = response.read()

# print(content)