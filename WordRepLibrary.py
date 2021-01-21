#
#   WordRepImport.py
#
#  Methods for loading in word representation data (GLoVe)
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
        self.library = pd.read_table(path, sep=' ', keep_default_na=False,
            index_col=0, quoting=csv.QUOTE_NONE, encoding="utf8", header=None)
        t = (time.time() - start_time)
        print("Loading word representation library took "+str(t)+" seconds.\n")
        self.n_words = self.library.shape[0]
        self.ci_roots = None
        self.ci_vocab = None

    # Get a specific word representation by integer count index
    def get_wrep_by_int(self, i):
        return list(self.library.iloc[i])

    # Get a specific word representation
    def get_wrep(self, word):
        return list(self.library.loc[word])

    # Get a specific word representation and it's index
    def get_wrepi(self, w, ignore_case_if_missing=True):
        if ignore_case_if_missing and w not in self.library.index:
            w = self.autocorrect_word(w)
        return self.library.index.get_loc(w), self.get_wrep(w)

    # Autocorrect a word to match a word in this library
    def autocorrect_word(self, word):
        self._build_autocorrect_index()
        return self.ci_roots[word_root(word)]

    def _build_autocorrect_index(self):
        if self.ci_roots is None:
            print("Constructing capitalisation autocorrection index...")
            roots = {}
            for w in self.library.index:
                r = word_root(w)
                if r not in roots: roots[r] = []
                roots[r].append(w)
            self.ci_roots = {w: sorted(roots[w])[-1] for w in roots}
            print("Completed.")

    # Adjust capitalisation autocorrection index to use 1gram count modes (+++)
    def import_autocorrect_1grams(self, ngrams_db):
        print("Importing 1gram capitalisation autocorrection index...")
        self._build_autocorrect_index()
        ngrams_db_roots = dict(list(zip(list(map(word_root,
            ngrams_db.index.values)), ngrams_db.index.values)))
        for r in self.ci_roots:
            if r in ngrams_db_roots:
                w = ngrams_db_roots[r]
                if w in self.library.index:
                    self.ci_roots[r] = w
        print("Completed 1grams import.")

    # Get a specific word representation and it's index if it exists
    def get_wrepi_if_exists(self, word):
        return self.get_wrepi(word) if word in self.library.index else None

    # Check if a word exists in the library
    def get_exists(self, word):
        return word in self.library.index

    # Same but ignoring case (assumes input word is all lowercase)
    def get_exists_ci(self, word):
        if self.ci_vocab is None:
            print("Case-insensitive vocabulary for representation library...")
            self.ci_vocab = set([w.lower() for w in self.library.index])
            print("Completed")
        return word in self.ci_vocab

    # Get a new, random unseen word from the library
    def get_new_word(self, i_seen=None, autocorrect_caps=True):

        # Get a random word (index) to add (that we haven't added yet)
        word_i = None
        if i_seen is None:
            word_i = np.random.randint(0, self.n_words)
        else:
            i_rem = [i for i in range(self.n_words) if i not in i_seen]
            word_i = i_rem[np.random.randint(0, len(i_rem))]

        word = self.library.index[word_i]
        if autocorrect_caps:
            word = self.autocorrect_word(word)
            return (word,) + self.get_wrepi(word)

        return word, word_i, self.get_wrep_by_int(word_i)


