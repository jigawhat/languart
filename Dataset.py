#
#  Data.py
#
# Methods for getting/adding data (words with sketchability etc)
#


from collections import OrderedDict

from Utils import *
from Constants import *
from DataRequests import *


class Dataset():

    def __init__(self, path, Y_labels=labels_de, X_labels=None):
        self.path = path
        self.Y_labels = Y_labels
        self.X_labels = X_labels

        # Import default dataset (data.csv) (will create if missing)
        self.df = None
        if os.path.exists(self.path):
            self.df = pd.read_csv(self.path, sep='\t', index_col=0)

    def save(self):
        return self.df.to_csv(self.path, sep='\t')

    def load(self):
        return self.df

    # Refresh the google search results count for each word
    # in the dataset. Also saves the timestamp in path.txt once complete.
    def refresh_gsearch_counts(self):
        l = len(self.df)
        driver = webdriver.Chrome()
        for i in range(l):
            sys_print("Refreshing google search counts: " + \
                str(i + 1) + '/' + str(l))
            word = self.df.index[i]
            print(word)
            num = google_search_count(word, driver)
            self.df.iloc[i]['gsc'] = num
        driver.close()
        with open(self.path + '.txt', 'w') as f:
            f.write(str(int(get_curr_ts())))
    print('\nComplete')

    # Add new word with given library index, x and y valuez
    def add_word(self, word, word_i, y, x):

        # If no data yet, create new dataset
        if self.df is None:

            # Get column labels
            if self.Y_labels is None:
                self.Y_labels = ['y' + str(i) for i in range(len(y))]
            if self.X_labels is None:
                self.X_labels = ['x' + str(i) for i in range(len(x))]
            labels = ["word"] + self.Y_labels + ["lib_i"] + self.X_labels

            # Create dataset from first entry
            data = OrderedDict(zip(labels, [word] + y + [word_i] + x))
            self.df = pd.DataFrame([data])
            self.df = self.df.set_index(["word"])

        # Else just add new entry
        else:
            self.df.loc[word] = y + [word_i] + x

        # Save new csv
        return self.save()


