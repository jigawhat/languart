#
# add_words.py
#
# This script allows the user to randomly sample the word library for new
# words, assign them "drawability" scores, and add them to the working dataset
#


import pandas as pd
from Utils import *


# Constants
data_dir = "data/"
data_csv = "data.csv"


# Import default dataset (data.csv)
words_df = pd.read_csv(data_dir + data_csv, index_col=0)



# Define add_word function
def add_word(dataset):
