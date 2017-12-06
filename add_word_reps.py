
 # Script for merging word representation libraries for words in the current
 # data_csv. The word representation libraries to add representations from are
 # specified in Constants.py


# TODO: make (a version of?) this script load each library and add
# representations in series rather than in parallel, to save on RAM


import pandas as pd
from copy import deepcopy

from Utils import *
from WordRepLibrary import *
from Dataset import *
from Constants import *


# Add path prefixes
lib_paths = [data_dir + word_rep_dir + path for path in lib_paths]

# Load existing dataset (script wont work if none exists)
dataset = Dataset(data_csv)
df = dataset.load()

# Load new word representation libraries (may take a while)
libs = [ WordRepLibrary(path) for path in lib_paths ]

# Get new column names (for adding new data to dataframe)
new_cols = sum([[lib_names[i] + "_" + str(j)
    for j in range(libs[i].library.shape[1])] for i in
    range(len(libs))], [])

# Add placeholder data columns to dataframe
for col in new_cols:
    df[col] = None

old_len = df.shape[0]
dropped_words = []
print("Merging word representations...")

# Merge word representations from current data_csv and given word
# representation libraries to create a new combined_csv, containing only the
# words that have representations in all libraries
for word in deepcopy(list(df.index)):

    destroy = False
    combo_rep = []

    # Get word representation from each library
    for lib in libs:
        rep = lib.get_wrepi_if_exists(word)
        # If the word doesn't appear in all libraries, destroy entry
        if rep is None:
            destroy = True
            break
        combo_rep += rep[1]

    if destroy:
        dropped_words += [ word ]
        df.drop(word, inplace=True)
        continue

    # Otherwise, add new column data
    df.loc[word, new_cols] = combo_rep

# Save new dataframe to combined dataset csv file
df.to_csv(combined_csv)

new_len = df.shape[0]
print("Finished combining word representations")
print("Old dataset entries: " + str(old_len))
print("New dataset entries: " + str(new_len))
print("Dropped words (" + str(old_len - new_len) + "): " + str(dropped_words))


