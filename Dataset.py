#
#  Data.py
#
# Methods for getting/adding data (words with sketchability etc)
#


from collections import OrderedDict
from Utils import *
from Constants import *


class Dataset():

    def __init__(self, path, Y_labels=labels_default, X_labels=None):
        self.path = path
        self.Y_labels = Y_labels
        self.X_labels = X_labels

        # Import default dataset (data.csv) (will create if missing)
        self.df = None
        if os.path.exists(self.path):
            self.df = pd.read_csv(self.path, index_col=0)

    def save(self):
        return self.df.to_csv(self.path)

    def load(self):
        return self.df

    # Add new word with given library index, x and y values
    def add_word(self, word, word_i, y, x):

        # If no data yet, create new dataset
        if self.df is None:

            # Get column labels
            if self.Y_labels is None:
                self.Y_labels = ['y' + str(i) for i in range(len(y))]
            if self.X_labels is None:
                self.X_labels = ['x' + str(i) for i in range(len(x))]
            labels = ["word", "lib_i"] + self.Y_labels + self.X_labels

            # Create dataset from first entry
            data = OrderedDict(zip(labels, [word, word_i] + y + x))
            self.df = pd.DataFrame([data])
            self.df = self.df.set_index(["word"])

        # Else just add new entry
        else:
            self.df.loc[word] = [ word_i ] + y + x

        # Save new csv
        return self.save()


