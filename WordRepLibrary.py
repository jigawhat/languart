#
#   WordRepImport.py
#
# Methods for loading in word representation data (GLoVe)
#


import csv
import time
import numpy as np
from Utils import *


class WordRepLibrary(): # TODO: Fix code to display load time remaining

    # Import the word representation library (GLoVe)
    def __init__(self, path):
        print("Loading word representation library '"+path.split('/')[-1]+"'")
        start_time = time.time()
        self.library = pd.read_table(path, header=None, sep=' ',
                encoding="utf8", index_col=0, quoting=csv.QUOTE_NONE)

        # self.library = []
        # self.n_words = 0
        # with open(path, 'r', encoding="utf8") as glove_file:
        #     i = 0
        #     self.n_words = len([None for line in glove_file])
        #     glove_file.seek(0, 0)
        #     for line in glove_file:
        #         tokens = line[:-1].split(' ')
        #         self.library += [ (tokens[0], tokens[1:]) ]
        #         i += 1
        #         if i % 10000 == 0 or i == self.n_words:
        #             pc = round(100.0 * (float(i) / float(self.n_words)), 2)
        #             fr = float(self.n_words - i) / float(i)
        #             tr = (time.time() - start_time) * fr
        #             tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
        #               else str(round(tr, 2)) + ' second') + "s remaining)   "
        #             sys_print("\rLoaded words: " + str(i) + " / " + \
        #                    str(self.n_words) + " (" + str(pc) + "%, " + tr)

        # print("\nConverting word library into OrderedDict...")
        # self.library = OrderedDict(self.library)

        t = (time.time() - start_time)
        print("Loading word representation library took "+str(t)+" seconds.\n")
        self.n_words = self.library.shape[0]

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

    # Get a new, unseen word from the library
    def get_new_word(self, i_seen):

        # Get a random word (index) to add (that we haven't added yet)
        word_i = None
        if i_seen is None:
            word_i = np.random.randint(0, self.n_words)
        else:
            i_rem = [i for i in range(self.n_words) if i not in i_seen]
            word_i = i_rem[np.random.randint(0, len(i_rem))]

        word = self.library.index[word_i]
        return word, word_i, self.get_wrep_by_int(word_i)


