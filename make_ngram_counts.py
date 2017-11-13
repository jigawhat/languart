#
#   make_ngram_counts.py
#
# Count Google 1grams for the given time period (from the Constants file),
# output resulting dataframe to ngram_counts.csv (also from Constants.py)
#


import time
import glob
from Utils import *
from Constants import *


total_count_est = 18559155

proj_root = os.getcwd()
ngrams_csv = proj_root + '/' + ngrams_counts

os.chdir(ngrams_data)
files = glob.glob('*')
new_db = not os.path.exists(ngrams_csv)

i = 0
cur_word, cur_pc, cur_bc = None, None, None # Current word, page and book count

print("Loading word ngram files...")
start_time = time.time()


def add_line(word, year, count, book_c, ngram_counts_csv_file):
    global i, new_db, start_time, total_count_est, cur_word, cur_pc, cur_bc
    
    count, book_c = int(count), int(book_c)
    word = word.split('_')[0]
    if ',' in word:
        if word[-1] != ',':
            return
        word = word[:-1]
    word = word.lower()

    if word == cur_word:
        cur_pc += count
        cur_bc += book_c
    else:
        if i > 0:
            if new_db:
                ngram_counts_csv_file.write("word,count,book_c\n")
                new_db = False
            z = ','.join([str(x) for x in [cur_word, cur_pc, cur_bc]]) + '\n'
            ngram_counts_csv_file.write(z)

        cur_word, cur_pc, cur_bc = word, count, book_c
        i += 1
        if i % 10000 == 0 or i == total_count_est:
            pc = round(100.0 * (float(i) / float(total_count_est)), 2)
            fr = float(total_count_est - i) / float(i)
            tr = (time.time() - start_time) * fr
            tr = (str(round(tr / 60, 2)) + ' minute' if tr > 120 \
                  else str(round(tr, 2)) + ' second') + "s remaining)      "
            sys_print("\rLoaded word ngrams: " + str(i) + " / " + \
                   str(total_count_est) + " (" + str(pc) + "%, " + tr)


with open(ngrams_csv, 'a', encoding='utf-8') as ng_csv:
    for f in files:
        with open(f, 'r', encoding='utf-8') as ngram_file:
            for line in ngram_file:
                word, year, count, book_c = line.split('\t')
                year = int(year)
                if within(year, ngrams_count_period):
                    add_line(word, year, count, book_c, ng_csv)


print("\nn words: " + str(i))
t = (time.time() - start_time)
print("Done. Counting ngrams took " + str(round(t / 60, 2)) + " minutes.\n")


 