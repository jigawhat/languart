#
#   Fix capitalisation+hyphenation autocorrected word 
#   datapoints (1gram counts and GLoVe representation)
#


import pandas as pd

from Utils import *
from WordRepLibrary import *
from Dataset import *
from Constants import *
from DataRequests import *



### Initialisation ###

# Launch Webdriver (for viewing word descriptions from a Google search)
driver = webdriver.Chrome()

# Load existing dataset/create new
dataset = Wordset()
df = dataset.load()

# Load ngram counts database
print("Reading prefolded 1grams...")
ngrams_db_precomp = pd.read_csv(ngrams_csv_precomp, index_col="word",
    keep_default_na=False, dtype={
    **{k: str for k in ["word", "root", "type"]},
    **{k: float for k in ["total", "total_b", "last5", "last10", "last20"]},
    **{k: float for k in ["mean", "mode", "min", "max"]}})
ngrams_db_precomp = ngrams_db_precomp.sort_index()
ngrams_db = load_ngram_counts()
library = WordRepLibrary(word_rep_data)
library.import_autocorrect_1grams(ngrams_db)


to_correct = pd.read_csv(data_dir + '/no_autocorrect.tsv', sep='\t',
    index_col="word",
    dtype={"word": str, "ngrams": str, "gsearch": str, "representation:": str})
correct_roots = {word_root(w): to_correct.loc[w] for w in to_correct.index}


for w in df.index:
    r = word_root(w)
    if r in correct_roots:
        entry = correct_roots[r]
        new_w = entry.name

        # Get ngram counts for specific capitalisation/hyphenation
        if entry.ngrams != '0':
            w_ = new_w if entry.ngrams == '1' else entry.ngrams
            x = ngrams_db_precomp.loc[w_]
            if isinstance(x, pd.Series):
                x = pd.DataFrame(x).T
                x.index.name = "word"
            x_ = x[x.type == '?']
            if x_.shape[0] < 1: x_ = x
            arg_max = x_.iloc[np.argmax(x_["total"].values)]
            pos_filt = x[["type", "total"]].query("type == @pos_tags")
            pos_max = pos_filt.iloc[np.argmax(pos_filt["total"].values)].type \
                if pos_filt.shape[0] > 0 else '?'

            # Gather features
            df.loc[w, "ngc"] = arg_max["total"]
            df.loc[w, "nbc"] = arg_max["total_b"]
            df.loc[w, "mean"] = arg_max["mean"]
            df.loc[w, "mean_mode"] = arg_max["mode"]
            df.loc[w, "mode_mode"] = arg_max["mode"]
            df.loc[w, "min"] = arg_max["min"]
            df.loc[w, "max"] = arg_max["max"]
            df.loc[w, "last5"] = arg_max["last5"]
            df.loc[w, "last10"] = arg_max["last10"]
            df.loc[w, "last20"] = arg_max["last20"]
            df.loc[w, "type"] = pos_max
            print(w_ + " ngram counts added")

        # Get Google search results count
        if entry.gsearch != '0':
            w_ = new_w if entry.gsearch == '1' else entry.gsearch
            df.loc[w, "gsc"] = google_search_count(w_, driver=driver)
            print(w_ + " Google search count added")

        # Get GLoVe word representation
        if entry.representation != '0':
            w_ = new_w if entry.representation == '1' else entry.representation
            x = library.get_wrepi_if_exists(w_)
            if x is not None:
                df.loc[w, "lib_i"] = x[0]
                df.loc[w, X_rep_ls] = x[1]
                print(w_ + " representation added")
            else:
                print("Couldn't find corrected representation for: " + w_)

        # Fix capitalisation/hyphenation if variant is incorrect
        if w != new_w:
            print(new_w + " capitalisation/hyphenation corrected")
            df.rename(index={w: new_w}, inplace=True)

print("Autocorrect adjustments complete.")

dataset.save()
driver.close()


