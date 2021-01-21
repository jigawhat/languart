#
# add_words.py
#
# This script allows the user to randomly sample the word library for new
# words, assign them sketchability scores, and add them to the working dataset
#


import pandas as pd
from selenium import webdriver

from WordRepLibrary import *
from WordValidation import *
from Dataset import *


# Options
skip_google_search_viewer = False
skip_ngram_counts = False
skip_google_search_count = False
add_to_clipboard = False



# Launch Webdriver (for viewing word descriptions from a Google search)
if not skip_google_search_viewer:
    driver = webdriver.Chrome()

# Constants
google_search_url = "https://www.google.co.uk/search?q="



### Initialisation ###

# Load existing dataset/create new
dataset = Dataset(data_csv, labels_de)

# Load ngram counts database
ngrams_db = None
if not skip_ngram_counts:
    ngrams_db = load_ngram_counts()
library.import_autocorrect_1grams(ngrams_db)


### Add new words ###

print("\n *** Ready to add new words to dataset ***")
print(" *** Enter the random word characteristics (space-separated) or\n" + \
      "     enter a specific word by typing \"WORD:example 1 3.5 7 ...\"")
print('\n' + '\n'.join(l_key.split('\n')[:n_de_Y_labels]) + '\n')


try:
    while True:

        df = dataset.load()
        i_seen = None if df is None else list(df["lib_i"])

        word, word_i, x = library.get_new_word(i_seen, autocorrect_caps=True)

        # Skip word if not found in Google 1gram counts
        if not skip_ngram_counts and word not in ngrams_db.index:
            print("Word \""+ word +"\" skipped (not found in Google ngrams)")
            continue

        # Skip word if it contains non-english characters/punctuation,
        # or if the word cannot be found in the WordNet english dictionary
        if not valid_english(word):
            print("Word \""+ word +"\" skipped (not valid English)")
            continue
        if not valid_word(word):
            print("Skipping invalid word: " + word)
            continue

        # Send word to clipboard
        if add_to_clipboard:
            df_ = pd.DataFrame([word])
            df_.to_clipboard(index=False, header=False)

        # Until a valid input is entered, ask user for word data
        y, skip = None, False
        while True:
            # Get Y values from user
            y = input(
                "*** "+ word +" *** "+' '.join(labels_de[:-n_stat]) + " ::: ")
            if ' ' not in y and '\t' not in y:
                skip = True
                break
            y = y.split()

            # Add given word if specified
            if y[0][:5] == "WORD:":
                word = y[0][5:]
                if df is not None and word in list(df.index):
                    r = ''
                    while r != 'y' and r != 'n': 
                        r = input("Word already in database. " + \
                                  "Overwrite? (y/n)").lower()
                    if r == 'n':
                        skip = True
                        break
                if (not skip_ngram_counts) and word not in ngrams_db.index:
                    word = library.autocorrect_word(word)
                word_i, x = library.get_wrepi(word)
                y = y[1:]

            # Convert to number types
            y = [y_ for y_ in y if y_.replace('.', '').isnumeric()]
            y = [float(y_) for y_ in y]
            if len(y) == len(Y_types):
                break
            print("Invalid input, please try again:")

        if skip: continue
        for j in range(len(y)):
            if Y_types[j] is bool and y[j] != 0.0 and y[j] != 1.0:
                print("Word not added (non binary encountered)")
                continue

        # Add ngram word and book counts
        if not skip_ngram_counts:
            entry = list(ngrams_db.loc[word])
            y += [float(y_) for y_ in entry[1:]] + entry[:1]
        else:
            y += [-1 for i in range(len(ngc_cols))]

        # Add google search # of results for word
        num = -1
        if not skip_google_search_count:
            num = google_search_count(word, driver=driver)
        y += [ num ]

        # Check we have enough data
        print(y)
        if len(y) < len(labels_de):
            print("Word not added (not enough Y data given)")
            continue

        dataset.reload()
        dataset.add_word(word, word_i, y, x)
        dataset.save()
        print("******* \"" + word + "\" added. *******")

except Exception as e:
    pr_exception(e)
finally:
    driver.close()


