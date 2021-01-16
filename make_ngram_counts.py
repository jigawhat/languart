#
#   make_ngram_counts.py
#
# Count Google 1grams for the given time period (from the Constants file),
# output resulting dataframe to ngram_counts.csv (also from Constants.py)
#


import time
import glob
import numpy as np

from Utils import *
from Constants import *
from WordValidation import *


proj_root = os.getcwd()
ngrams_csv_path = proj_root + '/' + ngrams_csv_precomp

os.chdir(ngrams_data)
files = glob.glob('*')
new_db = not os.path.exists(ngrams_csv_path)

i, total_count = 0, 0

print("Loading word ngram files...")
start_time = time.time()

print("Counting number of 1grams...")
total_1grams = 59480430  # Precomputed for 2020 Google 1grams
#total_1grams = sum([sum(1 for _ in open(f, encoding='utf-8')) for f in files])
print("Number of 1grams: " + str(total_1grams))


def add_word(w, entries, out):
    global i, total_count, new_db, start_time, total_1grams
    
    word_type = "?"
    w = w.strip()
    if '_' in w:
        w = w.split('_')
        if w[-1] != '': word_type = w[-1]
        w = w[0]
    if w in allowed_words_countonly:
        w = w.replace('.', '')
    w_root = word_root(w)

    entries = [e.split(',') for e in entries]
    ys = np.asarray([float(y) for (y, _, _) in entries])
    ns = np.asarray([float(n) for (_, n, _) in entries])
    nb = np.asarray([float(n) for (_, _, n) in entries])
    min_, max_ = min(ys), max(ys)
    total, total_b = sum(ns), sum(nb)
    zipd = list(zip(ys, ns))
    mean = round(sum((y * float(n)) for (y, n) in zipd) / total, 3)
    mode = ys[(len(ys) - 1) - np.argmax(ns[::-1])] if max(ns) > 1 else mean
    total, total_b = int(total), int(total_b)
    last5  = int(sum([n for (y, n) in zipd if y >= last5_min]))
    last10 = int(sum([n for (y, n) in zipd if y >= last10_min]))
    last20 = int(sum([n for (y, n) in zipd if y >= last20_min]))

    if new_db:
        out.write("word,root,type," + \
                  "total,total_b,mean,mode,min,max,last5,last10,last20\n")
        new_db = False
    z = ','.join([str(x) for x in [w, w_root, word_type, total, total_b, \
        mean, mode, min_, max_, last5, last10, last20]]) + '\n'
    out.write(z)

    total_count += 1
    if i > 0 and i % 10000 == 0 or i == total_1grams:
        pc = round(100.0 * (float(i) / float(total_1grams)), 2)
        fr = float(total_1grams - i) / float(i)
        tr = (time.time() - start_time) * fr
        tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
              else str(round(tr, 2)) + ' second') + "s remaining)      "
        sys_print("\rLoaded word ngrams: " + str(total_count) + \
            ' (from ' + str(i) + " 1grams) / " + \
            str(total_1grams) + " (" + str(pc) + "%, " + tr)


with open(ngrams_csv_path, 'a', encoding='utf-8') as ng_csv:
    for f in files:
        with open(f, 'r', encoding='utf-8') as ngram_file:
            for line in ngram_file:
                entries = line.split('\t')
                w, max_year = entries[0], int(entries[-1].split(',')[0])
                min_year = int(entries[1].split(',')[0])
                if valid_word(strh(w, '_'), min_year) and \
                  within(max_year, ngrams_count_period):
                    add_word(w, entries[1:], ng_csv)
                i += 1


print("\nn words: " + str(total_count))
t = (time.time() - start_time)
print("Done. Counting ngrams took " + str(round(t / 60, 2)) + " minutes.\n")


 