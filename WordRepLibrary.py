#
#   WordRepImport.py
#
# Methods for loading in word representation data (GLoVe)
#


import time
import numpy as np
from Utils import *


class WordRepLibrary():

    def __init__(self, path):
        # Import the word library (GLoVe)
        self.library = []
        self.n_words = 0
        start_time = None
        with open(path, 'r', encoding="utf8") as glove_file:
            start_time = time.time()
            i = 0
            self.n_words = len([0 for line in glove_file])
            glove_file.seek(0, 0)
            for line in glove_file:
                tokens = line[:-1].split(' ')
                self.library += [ (tokens[0], tokens[1:]) ]
                i += 1
                if i % 10000 == 0:
                    sys_print("\rLoaded words: "+ \
                        str(i) + " / " + str(self.n_words))

        print("\nConverting word library into OrderedDict...")
        self.library = OrderedDict(self.library)
        t = (time.time() - start_time)
        print("Loading word library took " + str(t) + " seconds.\n")

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



