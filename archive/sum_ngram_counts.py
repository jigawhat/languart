#
#   sum_ngram_counts.py
#
# Sums the duplicate key entries in the ngram counts database
# 


import time
import pandas as pd
from Utils import *
from Constants import *


# Load ngram counts database
print("Loading ngram counts database...")

t = time.time()
ngrams_db = pd.read_csv(ngrams_counts, index_col=0, error_bad_lines=False)
t = (time.time() - t)

print("Loading ngram counts database took " + str(t) + " seconds.")
print("Number of words: " + str(len(ngrams_db.index)))
print("Summing duplicate word rows...")

ngrams_db.index = ngrams_db.index.str.lower()
t = time.time()
ngrams_db = ngrams_db.groupby(ngrams_db.index).sum()
t = (time.time() - t)

print("Summing duplicate word rows took " + str(t) + " seconds.")
print("New number of words: " + str(len(ngrams_db.index)))
print("Saving to csv file...")

ngrams_db.to_csv(ngrams_counts + '3', encoding='utf-8')


