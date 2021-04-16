#
#   Constants.py
#
#  Shared constants for project
#
from memory_profiler import profile
@profile(precision=4)
def func(n):
   return sum(range(n))
@profile(precision=4)
def func2(n):
   return sum(list(range(n)))

######## Data folder
data_dir = "data/"


######## Google Ngram counts data
ngrams_dir = "H:\\Code/ngrams/"
# ngrams_dir = data_dir + "ngrams/"
ngrams_data = ngrams_dir + "google_20200217_1grams/"
# ngrams_data = ngrams_dir + "google_20120701_1grams/"
ngrams_csv = data_dir + "ngram_counts.csv"
ngrams_csv_precomp = data_dir + "ngram_counts_precomp.csv"
listset_txt = data_dir + "examples.txt"
last5_min = 2015
last10_min = 2010
last20_min = 2000
ngrams_count_period = [2000, 2050]   # (words must have occured in this period)

########### Main word representation library
word_rep_dir = "word_reps/"
# word_rep_data = data_dir + word_rep_dir + "glove.6B/glove.6B.300d.txt"
word_rep_data = data_dir + word_rep_dir + "glove.840B/glove.840B.300d.txt"

########## Main working dataset
data_csv = data_dir + "data.tsv"
learning_data_dir = "learning_data/"   # Saved intermediate learning data

# Fields data types information
Y_labels_de = ['inc', 'dif', 'nrd', 'skt', 'vis', 'phy',
               'obj', 'com', 'spl', 'grp', 'edu', 'nym']
X_rep_ls = ['x' + str(i) for i in range(300)]
# X_rep_ls = ["g42B_300d" + '_' + str(i) for i in range(300)]

# Ngram counts - total and book count, year stats and recent counts
ngc_cols = ['ngc', 'nbc', 'mean', 'mean_mode', 'mode_mode',
            'min', 'max', 'last5', 'last10', 'last20', 'type']
gsc_col = 'gsc'             # Google search results count
X_labels_de = X_rep_ls + ngc_cols + [gsc_col]
labels_de = Y_labels_de + ngc_cols + [gsc_col]
Y_types = [float for _ in Y_labels_de]
n_stat = len(ngc_cols) + 1  # Number of x values suffixed to end of vector
n_de_Y_labels = (len(labels_de) - n_stat)  # Number of default Y labels

# Key
l_key = \
    " inc = Probability word should be included at all in its ideal game\n" + \
    " dif = Inverse difficulty (general intuitive comb of skt, spl & IQ)\n" + \
    " nrd = Recognisability / Inverse recognition difficulty\n" + \
    " skt = Sketchability (ease of sketching in pictionary)\n" + \
    " vis = Visuality (visual nature)\n" + \
    " phy = Physicality (physical nature)\n" + \
    " obj = Objectness (whether or not it is an object)\n" + \
    " com = Commonality (well-known-ness among younger age groups)\n" + \
    " spl = Specialisation level (depth of domain knowledge required)\n" + \
    " grp = Groupness (a single individual = 0, a domain of life = 10)\n" + \
    " edu = Degree of inclusion in curriculum or academia generally\n" + \
    " nym = Degree of homonymity (number of extra meanings * 3, cap 10)\n" + \
    " ngc = (Google) books corpus Ngram book count\n" + \
    " nbc = (Google) books corpus Ngram book count\n" + \
    " mean = Mean year of occurrence in Google ngrams \n" + \
    " mean_mode = Mean of cap. variants' mode of year of occurrence\n" + \
    " mode_mode = Mode of cap. variants' mode of year of occurrence\n" + \
    " min = Oldest year of occurrence\n" + \
    " max = Youngest year of occurrence\n" + \
    " last5 = Number of occurrences in the past 5 years\n" + \
    " last10 = Number of occurrences in the past 10 years\n" + \
    " last20 = Number of occurrences in the past 20 years\n" + \
    " type = Most common part of speech tag for word in Google ngrams\n" + \
    " gsc = Google search results count\n" + \
    ""

lprompts = [  # If includes "types of" we use the singular (non-plural) phrase
    "A list of",
    "A long list of",
    "An exhaustive list of",
    "A list of types of ",
    "Different",
    "A list of different",
    "A list of different types of",
    "A long list of different",
    "A long list of different types of",
    "An exhaustive list of different",
    "An exhaustive list of different types of",
    "Well-known",
    "A list of well-known",
    "A list of well-known types of",
    "A long list of well-known",
    "A long list of well-known types of",
    "An exhaustive list of well-known",
    "An exhaustive list of well-known types of",
    "Common",
    "A list of common",
    "A list of common types of",
    "A long list of common",
    "A long list of common types of",
    "An exhaustive list of common",
    "An exhaustive list of common types of",
    "Some",
    "A list of some",
    "A list of some types of",
    "A long list of some",
    "A long list of some types of",
    "An exhaustive list of some",
    "An exhaustive list of some types of",
] 

# Part of speech tagset for Google ngrams (frequency and % in comment)
# Note: the frequency data is somewhat unprocessed
pos_tags = [
    # "X",     #   4562969893          (   0.15%   )  # ( Other - disabled )
    # "NUM",   #   10359909952         (   0.33%   )  # ( Number - disabled )
    "PRT",     # 45361608405           (   1.45%   )
    "CONJ",    #    60763767404        (   1.95%   )
    "ADV",     # 71401527469           (   2.29%   )
    "PRON",    #    75534024221        (   2.42%   )
    "ADJ",     # 128073334803          (   4.11%   )
    "DET",     # 184719428708          (   5.92%   )
    "ADP",     # 216548456584          (   6.94%   )
    "VERB",    #    249754507701       (   8.00%   )
    "NOUN",    #   1559809008954       (   16.42%  )
]



# Additional word representation libraries (for add_word_reps.py)
# lib_names = [
#                 "g6B_50d",
#                 "g6B_100d",
#                 "g6B_200d",
#                 "g42B_300d",
# ]
# lib_paths = [
#                 "glove.6B/glove.6B.50d.txt",
#                 "glove.6B/glove.6B.100d.txt",
#                 "glove.6B/glove.6B.200d.txt",
#                 "glove.42B.300d.txt",
# ]
# lib_paths = [data_dir + word_rep_dir + path for path in lib_paths]

# # Name of combined word representation data_csv created by add_word_reps.py
# combined_csv = data_dir + "data_combi.csv"

# X_labels_de = ["x" + str(n) for n in range(10 ** 3)] + \
#     sum([[l + str(n) for n in range(10 ** 3)] for l in lib_names], [])

