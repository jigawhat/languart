#
#  Shared data request methods
#

import time
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet

from Utils import *
from Constants import *


# Load WordNet dictionary
nltk.download('wordnet')


# Function to check word is valid english
def valid_english(word, verbose=True):
    for char in word:
        ordi = ord(char)
        if(ordi >= 127 or ordi < 33):
            if verbose:
                print("Word \"" + word + "\" skipped (language/symbols)")
            return False
    if not wordnet.synsets(word):
        if verbose:
            print("Word \"" + word + "\" skipped (not an English word)")
        return False
    return True


# Function to return number of Google search results of given query string
def google_search_count(query, driver=None):
    URL     = "https://www.google.com/search?q=" + query
    new_driver = False
    if driver is None:
        new_driver = True
        driver = webdriver.Chrome()
    success = False
    while not success:
        try:
            driver.get(URL)
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            total_results_text = soup.find("div",
                {"id": "result-stats"}).find(text=True, recursive=False)
            res = ''.join([num for num in total_results_text if num.isdigit()])
            success = True
        except Exception as e:
            pr_exception(e)
            print("Press Enter to continue, " + \
                "once captcha or other issue is resolved...")
            input()
    if new_driver:
        driver.close()
    return int(res)


# Load ngram counts tsv into pandas dataframe
def load_ngram_counts():
    sys_print("\nLoading ngram counts database...")
    start_time = time.time()
    ngrams_db = pd.read_csv(ngrams_csv, index_col="word",
        error_bad_lines=False, keep_default_na=False, encoding='utf-8',
        dtype={k: str for k in ngc_cols})
    t = (time.time() - start_time)
    sys_print("\rLoading ngram counts database... " + \
              str(len(list(ngrams_db.index))) + " entries")
    print("\nLoading ngram counts database took " + str(t) + " seconds.")
    return ngrams_db


