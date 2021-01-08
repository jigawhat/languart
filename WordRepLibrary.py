#
#   WordRepImport.py
#
# Methods for loading in word representation data (GLoVe)
#


import csv
import time
import numpy as np

from Utils import *


class WordRepLibrary():

    # Import the word representation library (GLoVe)
    def __init__(self, path):
        print("Loading word representation library '"+path.split('/')[-1]+"'")
        start_time = time.time()
        self.library = pd.read_table(path,header=None, sep=' ',encoding="utf8",
            index_col=0, quoting=csv.QUOTE_NONE, keep_default_na=False)
        t = (time.time() - start_time)
        print("Loading word representation library took "+str(t)+" seconds.\n")
        self.n_words = self.library.shape[0]
        self.ci_vocab = None

    # Get a specific word representation by integer count index
    def get_wrep_by_int(self, i):
        return list(self.library.iloc[i])

    # Get a specific word representation
    def get_wrep(self, word):
        return list(self.library.loc[word])

    # Get a specific word representation and it's index
    def get_wrepi(self, word):
        return self.library.index.get_loc(word), \
               self.get_wrep(word)

    # Get a specific word representation and it's index if it exists
    def get_wrepi_if_exists(self, word):
        return self.get_wrepi(word) if word in self.library.index else None

    # Check if a word exists in the library
    def get_exists(self, word):
        return word in self.library.index

    # Same but ignoring case (assumes word is lowercase already)
    def get_exists_ci(self, word):
        if self.ci_vocab is None:
            print("Case-insensitive vocabulary for representation library...")
            self.ci_vocab = set([w.lower() for w in self.library.index])
        return word in self.ci_vocab

    # Get a new, random unseen word from the library
    def get_new_word(self, i_seen=None):

        # Get a random word (index) to add (that we haven't added yet)
        word_i = None
        if i_seen is None:
            word_i = np.random.randint(0, self.n_words)
        else:
            i_rem = [i for i in range(self.n_words) if i not in i_seen]
            word_i = i_rem[np.random.randint(0, len(i_rem))]

        word = self.library.index[word_i]
        return word, word_i, self.get_wrep_by_int(word_i)


