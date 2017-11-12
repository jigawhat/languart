#
# add_words.py
#
# This script allows the user to randomly sample the word library for new
# words, assign them sketchability scores, and add them to the working dataset
#


from Utils import *
from WordRepLibrary import *
from Dataset import *
from Constants import *


# Constants
data_path = data_dir + data_csv
word_lib_path = data_dir + glove_data
Y_labels = Y_labels_default



### Initialisation ###

# Load existing dataset/create new
dataset = Dataset(data_path, Y_labels)

# Load word representation library
library = WordRepLibrary(word_lib_path)



### Add new words ###

while True:

    df = dataset.load()
    i_seen = None if df is None else list(df["lib_i"])

    word, word_i, x = library.get_new_word(i_seen)

    ys = input("*** " + word + " *** " + ' '.join(Y_labels) + " ::: ")
    if ' ' not in ys or len(ys.split(' ')) < len(Y_labels):
        # Skip word if invalid response received
        print("Word skipped")
        continue

    y = [float(n) for n in ys.split(' ')]

    dataset.add_word(word, word_i, y, x)


