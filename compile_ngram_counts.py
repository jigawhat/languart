#
#  Compile 1gram counts tsv so that each word occurs only once, using the most common capitalisation
#  This should be run once after make_ngram_counts.py
#

import time
import numpy as np

from Utils import *
from Constants import *

proj_root = os.getcwd()
ngrams_csv_path = proj_root + '/' + ngrams_csv
print("Reading precompiled 1grams...")
ngrams_db = pd.read_csv(ngrams_csv_precomp, index_col="word")

with open(ngrams_csv_path, 'a', encoding='utf-8') as out:

    if not os.path.exists(ngrams_csv_path):
        out.write("word,total,total_b," + \
            "mean,mean_mode,mode_mode,min,max,last5,last10,last20\n")

    print("Compiling 1grams...")
    i = 0
    uniq = list(ngrams_db.root.unique())
    n_uniq = len(uniq)
    start_time = time.time()
    for w in uniq:
        x = ngrams_db[ngrams_db['root'] == w]
        x__ = []
        for w_ in list(x.index.unique()):
            x_ = x[x.index == w_]
            i = np.argmax(x_["total"].values)
            x__.append(x_.iloc[i])
        x = pd.DataFrame(x__)
        arg_max = x.iloc[np.argmax(x["total"].values)]

        word = arg_max.name
        total = sum(x["total"])
        total_b = sum(x["total_b"])
        mean = sum(x["mean"] * (x["total"] / total))
        mean_mode = sum(x["mode"] * (x["total"] / total))
        mode_mode = int(arg_max["mode"])
        min_ = int(min(x["min"]))
        max_ = int(max(x["max"]))
        last5 = sum(x["last5"])
        last10 = sum(x["last10"])
        last20 = sum(x["last20"])
        
        z = ','.join([str(x) for x in [word, total, total_b, mean, \
            mean_mode, mode_mode, min_, max_, last5, last10, last20]]) + '\n'
        out.write(z)
        i += 1
        if i > 0 and i % 10000 == 0 or i == n_uniq:
            pc = round(100.0 * (float(i) / float(n_uniq)), 2)
            fr = float(n_uniq - i) / float(i)
            tr = (time.time() - start_time) * fr
            tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
                  else str(round(tr, 2)) + ' second') + "s remaining)      "
            sys_print("\rLoaded word ngrams: " + str(i) + " / " + \
                str(n_uniq) + " (" + str(pc) + "%, " + tr)

