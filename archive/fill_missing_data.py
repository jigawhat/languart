
 # Script for adding missing Google ngram and search results count data.
 # Automatically finds missing entries in data_csv and fills them in


import pandas as pd
from copy import deepcopy

from Utils import *
from WordRepLibrary import *
from Dataset import *
from Constants import *
from DataRequests import *


# Load current dataset
data = Wordset()

# Load ngram counts database
ngrams_db = load_ngram_counts()


# Get all words in dataset which have some missing data (< 0 fields)
ngc_words = list(set(list(data.df[data.df[ngc_cols[0]] < 0].index)) | \
                 set(list(data.df[data.df[ngc_cols[1]] < 0].index)))
gsc_words = list(data.df[data.df[gsc_col] < 0].index)


# Fill in missing ngram count data
for word in ngc_words:

    if word not in ngrams_db.index:
        print("Word '" + word + "' not found in ngram count db, dropping...")
        gsc_words.remove(word)
        data.df.drop(word, inplace=True)
        continue

    ngcs = list(ngrams_db.loc[word])
    data.df.loc[word, ngc_cols] = ngcs
    print("Added ngram counts for word '" + word + "': " + str(ngcs))

# Fill in missing google search results count data
for word in gsc_words:
    gsc = google_search_count(word)
    data.df.loc[word, gsc_col] = gsc
    print("Added google search count for word '" + word + "': " + str(gsc))

# Check with user that changes are ok to save
input("Press enter to save changes, otherwise Ctrl-C to cancel")
data.save()


