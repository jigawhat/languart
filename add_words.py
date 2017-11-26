#
# add_words.py
#
# This script allows the user to randomly sample the word library for new
# words, assign them sketchability scores, and add them to the working dataset
#


import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import nltk
from nltk.corpus import wordnet

from Utils import *
from WordRepLibrary import *
from Dataset import *
from Constants import *


# Load WordNet dictionary
nltk.download('wordnet')

# Launch Webdriver (for viewing word descriptions from a Google search)
driver = webdriver.Chrome("C:/Users/Fonz/Code/chromedriver.exe")

# Constants
labels = labels_default
google_search_url = "https://www.google.co.uk/search?q="


### Initialisation ###

# Load existing dataset/create new
dataset = Dataset(data_csv, labels)

# Load ngram counts database
sys_print("\nLoading ngram counts database...")
start_time = time.time()
ngrams_db = pd.read_csv(ngrams_counts, index_col="word",
                        error_bad_lines=False, encoding='utf-8')
t = (time.time() - start_time)
sys_print("\rLoading ngram counts database... " + \
          str(len(list(ngrams_db.index))) + " entries")
print("\nLoading ngram counts database took " + str(t) + " seconds.")

# Load word representation library
print()
library = WordRepLibrary(word_rep_data)



### Add new words ###

print("\n *** Ready to add new words to dataset ***")
print(" *** Enter the random word characteristics (space-separated) or\n" + \
      "     enter a specific word by typing \"WORD:example 1 3.5 7 ...\"")
print('\n' + '\n'.join(l_key.split('\n')[:n_y]) + '\n')

while True:

    df = dataset.load()
    i_seen = None if df is None else list(df["lib_i"])

    word, word_i, x = library.get_new_word(i_seen)

    # Skip word if not found in Google 1gram counts
    if word not in ngrams_db.index:
        continue

    # Skip word if it contains non-english characters/punctuation,
    # or if the word cannot be found in the WordNet english dictionary
    skip = False
    for char in word:
        ordi = ord(char)
        if(ordi >= 127 or ordi < 33):
            print("Word \"" + word + "\" skipped (language/symbols)")
            skip = True
            break
        elif(not wordnet.synsets(word)):
            print("Word \"" + word + "\" skipped (not an English word)")
            skip = True
            break
    if skip: continue

    # Send word to clipboard
    df_ = pd.DataFrame([word])
    df_.to_clipboard(index=False, header=False)

    # Open google search page for word in Chrome
    driver.get(google_search_url + word)

    # Until a valid input is entered, ask user for word data
    y = None
    while True:
        # Get Y values from user
        y = input("*** " + word + " *** " + ' '.join(labels[:-n_stat])+" ::: ")
        if ' ' not in y:
            skip = True
            break
        y = y.split(' ')

        # Add given word if specified
        if y[0][:5] == "WORD:":
            word = y[0][5:]
            if df is not None and word in list(df.index):
                r = ''
                while r != 'y' and r != 'n': 
                    r = input("Word already in database. " + \
                              "Overwrite? (y/n)").lower()
                if r == 'n':
                    skip = True
                    break
            word_i, x = library.get_word(word)
            y = y[1:]

        # Convert to number types
        y = [y_ for y_ in y if y_.replace('.','').isnumeric()]
        y = [float(y_) for y_ in y]
        if len(y) == len(Y_types):
            break
        print("Invalid input, please try again:")

    if skip: continue
    for j in range(len(y)):
        if Y_types[j] is bool and y[j] != 0.0 and y[j] != 1.0:
            print("Word not added (non binary encountered)")
            continue

    # Add ngram word and book counts to y (easier for adding to dataset than x)
    y += [int(y_) for y_ in list(ngrams_db.loc[word])]

    # Add google search # of results for word (again, technically an x value)
    r = requests.get("https://www.google.com/search", params={'q': word})
    soup = BeautifulSoup(r.text, "lxml")
    res = soup.find("div", {"id": "resultStats"})
    num = res.text.split(' ')
    num = num[0] if len(num) < 3 else num[1]
    num = int(num.replace(',', ''))
    if num <= 5:
      num = 0
    y += [ num ]

    # Check we have enough data
    print(y)
    if len(y) < len(labels):
        print("Word not added (not enough Y data given)")
        continue

    dataset.add_word(word, word_i, y, x)
    print("******* \"" + word + "\" added. *******")


