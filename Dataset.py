#
#  Data.py
#
# Methods for getting/adding data (words with sketchability etc)
#


from collections import OrderedDict
from Utils import *


class Dataset():

    def __init__(self, path, Y_labels=None, X_labels=None):
        self.path = path
        self.Y_labels = Y_labels
        self.X_labels = X_labels

        # Import default dataset (data.csv) (will create if missing)
        self.data_df = None
        if os.path.exists(self.path):
            self.data_df = pd.read_csv(self.path, index_col=0)

    def load(self):
        return self.data_df

    def add_word(self, word, word_i, y, x):

        # If no data yet, create new dataset
        if self.data_df is None:

            # Get column labels
            if self.Y_labels is None:
                self.Y_labels = ['y' + str(i) for i in range(len(y))]
            if self.X_labels is None:
                self.X_labels = ['x' + str(i) for i in range(len(x))]
            labels = ["word", "lib_i"] + self.Y_labels + self.X_labels

            # Create dataset from first entry
            data = OrderedDict(zip(labels, [word, word_i] + y + x))
            self.data_df = pd.DataFrame([data])
            self.data_df = self.data_df.set_index(["word"])

        # Else just add new entry
        else:
            self.data_df.loc[word] = [ word_i ] + y + x

        # Save new csv
        self.data_df.to_csv(self.path)


