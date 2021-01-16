#
#  Fold 1gram counts csv so that each word occurs only once, using the most
#  common capitalisation. This should be run once after make_ngram_counts.py
#

import time
import numpy as np

from Utils import *
from Constants import *


# Options
skip_existing = True      # Whether to skip words already in the ngrams dataset
flush_every_line = True   # Whether to flush append output every new line, so
                          # that multiprocess script instances do not interfere


start_i = int(sys.argv[1]) if len(sys.argv) > 1 else 0  # Custom start/end idxs
end_i = int(sys.argv[2]) if len(sys.argv) > 2 else None

proj_root = os.getcwd()
ngrams_csv_path = proj_root + '/' + ngrams_csv
print("Reading prefolded 1grams...")
ngrams_db = pd.read_csv(ngrams_csv_precomp, index_col="root",
    keep_default_na=False, dtype={
    **{k: str for k in ["word", "root", "type"]},
    **{k: float for k in ["total", "total_b", "last5", "last10", "last20"]},
    **{k: float for k in ["mean", "mode", "min", "max"]}})
ngrams_db = ngrams_db.sort_index()

# Importing existing words
existing = []
new_dataset = not os.path.exists(ngrams_csv_path)
if skip_existing and not new_dataset:
    existing = set(map(word_root, list(pd.read_csv(ngrams_csv_path,
        index_col="word", keep_default_na=False, low_memory=False).index)))

# Identify words to fold
uniq = sorted(list(ngrams_db.index.unique()))
n_uniq = len(uniq)
if end_i is None: end_i = n_uniq
if skip_existing: uniq = [w for (k, w) in enumerate(uniq) if \
    k >= start_i and k < end_i and (w not in existing)]
n_doing = len(uniq)

with open(ngrams_csv_path, 'a', encoding='utf-8') as out:

    # Write header
    if new_dataset:
        out.write("word,type,ngc,nbc," + \
            "mean,mean_mode,mode_mode,min,max,last5,last10,last20\n")
        out.flush()

    i = 0
    gc.collect()
    print("Folding 1grams " + str(start_i) + " to " + str(end_i) + "...")
    start_time = time.time()
    for w in uniq:
        i += 1

        # Filter data for word & most common capitalisation
        x = ngrams_db.loc[w]
        if isinstance(x, pd.Series):
            x = pd.DataFrame(x).T
            x.index.name = "root"
        x__ = []
        x_v = {}  # Word part of speech variants stored for top type extraction
        uniq_variants = list(x.word.unique())
        for w_ in uniq_variants:
            x_ = x[x.word == w_]
            x_v[w_] = x_
            x__.append(x_.iloc[np.argmax(x_["total"].values)])
        x = pd.DataFrame(x__)
        word, arg_max, pos_max = None, None, 'ERROR'
        try:  # No more errors observed; just in case
            x_ = x[x.type == '?']
            if x_.shape[0] < 1: x_ = x
            arg_max = x_.iloc[np.argmax(x_["total"].values)]
            word = arg_max.word
            pos_filt = x_v[word][["type", "total"]].query("type == @pos_tags")
            pos_max = pos_filt.iloc[np.argmax(pos_filt["total"].values)].type \
                if pos_filt.shape[0] > 0 else '?'
        except Exception as e:
            pr_exception(e)
            continue

        # Gather features
        total = int(sum(x["total"]))
        total_b = int(sum(x["total_b"]))
        mean = round(sum(x["mean"] * (x["total"] / total)), 3)
        mean_mode = round(sum(x["mode"] * (x["total"] / total)), 3)
        mode_mode = int(arg_max["mode"])
        min_ = int(min(x["min"]))
        max_ = int(max(x["max"]))
        last5 = int(sum(x["last5"]))
        last10 = int(sum(x["last10"]))
        last20 = int(sum(x["last20"]))
        
        # Output to file
        z = ','.join([str(x) for x in [word, pos_max, total, total_b, mean, \
            mean_mode, mode_mode, min_, max_, last5, last10, last20]]) + '\n'
        out.write(z)
        if flush_every_line: out.flush()

        # Print progress
        if (i % 100 == 0 or i == (n_doing - 1)) and i > 0:
            pc = round(100.0 * (float(i) / float(n_doing)), 2)
            fr = float(n_doing - i) / float(i)
            tr = (time.time() - start_time) * fr
            tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
                  else str(round(tr, 2)) + ' second') + "s remaining)      "
            sys_print("\rLoaded word ngrams: " + str(i) + " / " + \
                str(n_doing) + " (" + str(pc) + "%, " + tr)

print("\nFinished")
