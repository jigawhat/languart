#
#  Shared data request methods
#

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet

from Utils import *
from Constants import *


# Load WordNet dictionary
nltk.download('wordnet')


# Function to return number of Google search results of given query string
def google_search_count(query):
    r = requests.get("https://www.google.com/search", params={'q': query})
    soup = BeautifulSoup(r.text, "lxml")
    res = soup.find("div", {"id": "resultStats"})
    res = res.text.split(' ')
    res = res[0] if len(res) < 3 else res[1]
    res = int(res.replace(',', ''))
    return res if res > 5 else 0


# Load ngram counts csv into pandas dataframe
def load_ngram_counts():
    sys_print("\nLoading ngram counts database...")
    start_time = time.time()
    ngrams_db = pd.read_csv(ngrams_counts, index_col="word",
                            error_bad_lines=False, encoding='utf-8')
    t = (time.time() - start_time)
    sys_print("\rLoading ngram counts database... " + \
              str(len(list(ngrams_db.index))) + " entries")
    print("\nLoading ngram counts database took " + str(t) + " seconds.")
    return ngrams_db


