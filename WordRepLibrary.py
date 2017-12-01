#
#   WordRepImport.py
#
# Methods for loading in word representation data (GLoVe)
#


import time
import numpy as np
from Utils import *


class WordRepLibrary(): # TODO: Create alternate version for 5GB+ libraries

    # Import the word representation library (GLoVe)
    def __init__(self, path):
        self.library = []
        self.n_words = 0
        start_time = None
        print("Loading word representation library '"+path.split('/')[-1]+"'")
        with open(path, 'r', encoding="utf8") as glove_file:
            start_time = time.time()
            i = 0
            self.n_words = len([None for line in glove_file])
            glove_file.seek(0, 0)
            for line in glove_file:
                tokens = line[:-1].split(' ')
                self.library += [ (tokens[0], tokens[1:]) ]
                i += 1
                if i % 10000 == 0 or i == self.n_words:
                    pc = round(100.0 * (float(i) / float(self.n_words)), 2)
                    fr = float(self.n_words - i) / float(i)
                    tr = (time.time() - start_time) * fr
                    tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
                      else str(round(tr, 2)) + ' second') + "s remaining)     "
                    sys_print("\rLoaded words: " + str(i) + " / " + \
                           str(self.n_words) + " (" + str(pc) + "%, " + tr)

        print("\nConverting word library into OrderedDict...")
        self.library = OrderedDict(self.library)
        t = (time.time() - start_time)
        print("Loading word representation library took "+str(t)+" seconds.\n")

    # Get a specific word representation
    def get_word(self, word):
        return list(self.library.keys()).index(word), \
               [float(x) for x in self.library[word]]

    # Get a specific word representation if it exists
    def get_word_if_exists(self, word):
        return self.get_word(word) if word in self.library.keys() else None

    # Get a new, unseen word from the library
    def get_new_word(self, i_seen):

        # Get a random word (index) to add (that we haven't added yet)
        word_i = None
        if i_seen is None:
            word_i = np.random.randint(0, self.n_words)
        else:
            i_rem = [i for i in range(self.n_words) if i not in i_seen]
            word_i = i_rem[np.random.randint(0, len(i_rem))]

        word = list(self.library.keys())[word_i]
        return word, word_i, [float(x) for x in self.library[word]]


