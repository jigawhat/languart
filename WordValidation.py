#
#  Word validation
#

import string

from Constants import *
from WordRepLibrary import *

# "‒―—"

alphabet_chars = string.ascii_lowercase + string.ascii_uppercase
allowed_chars = alphabet_chars + '0123456789' + '-'

# For these words, fullstops are removed prior to counting (share counts)
allowed_words_countonly = set(["N.W.A.", "R.E.M."])  
# Conflicting cases (National Wrestling Asc. 1930, rem as latin for thing)
disallowed_words = set(["NWA", "rem"])
allowed_words = ["AC/DC", "A&E", "B&B", "Q&A", "R&B",
    "will.i.am", "2Pac", "007", "42", "3.14"] + \
    ["19" + str(n) + "0s" for n in range(6, 10)] + ["2000s", "2010s"]
allowed_words = set([w.lower() for w in allowed_words])|allowed_words_countonly

words_27B = data_dir+word_rep_dir+"glove.twitter.27B/glove.twitter.27B.25d.txt"
library = WordRepLibrary(word_rep_data)  # From common crawl pre-2012
library2 = WordRepLibrary(words_27B)     # From Twitter pre-2012

# Assuming new terms are rare and therefore efficient to include here
def valid_word(w, min_year=0):
    if len(w) < 1: return False
    if w[0] == '-' or w[-1] == '-': return False
    w_lower = w.lower()
    return ((min_year >= 2012) or library.get_exists_ci(w_lower) or \
        library2.get_exists_ci(w_lower) or (w_lower in allowed_words)) and \
        ((all([c in allowed_chars for c in w]) and w[0] in alphabet_chars) or \
        w_lower in allowed_words) and w not in disallowed_words


