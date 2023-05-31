"""
Author: Aleksa Zatezalo
Date: May 22th 2023
Description: A credential brute forcer written in python.
"""

import queue
import requests
import threading
import sys

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENTIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = "http://testphp.vulnweb.com"
THREADS = 50
WORDLIST = "./all.txt"

words = queue.Queue()

def get_words(resume=None):
    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')
        for extention in EXTENTIONS:
            words.put(f'/{word}{extention}')
    
    found_resume = False
    with open(WORDLIST) as f:
        raw_words = f.read()
        for word in raw_words.split():
            if resume is not None:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
            else:
                print(word)
                extend_words(word)
        return words

def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('v'); sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')

if __name__ == '__main__':
    words = get_words()
    print('Press any key to continue.')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()