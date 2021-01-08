#
#   Constants.py
#
# Shared constants for project
#


######## Data folder
data_dir = "data/"


######## Google Ngram counts data
ngrams_dir = "H:\\Code/ngrams/"
# ngrams_dir = data_dir + "ngrams/"
ngrams_data = ngrams_dir + "google_20200217_1grams/"
# ngrams_data = ngrams_dir + "google_20120701_1grams/"
ngrams_csv = data_dir + "ngram_counts.csv"
ngrams_csv_precomp = data_dir + "ngram_counts_precomp.csv"
last5_min = 2015
last10_min = 2010
last20_min = 2000
ngrams_count_period = [2000, 2050]   # (words must have occured in this period)


########### Main word representation library
word_rep_dir = "word_reps/"
# word_rep_data = data_dir + word_rep_dir + "glove.6B/glove.6B.300d.txt"
word_rep_data = data_dir + word_rep_dir + "glove.840B/glove.840B.300d.txt"

# Additional word representation libraries (for add_word_reps.py)
lib_names = [
                "g6B_50d",
                "g6B_100d",
                "g6B_200d",
                "g42B_300d",
]
lib_paths = [
                "glove.6B/glove.6B.50d.txt",
                "glove.6B/glove.6B.100d.txt",
                "glove.6B/glove.6B.200d.txt",
                "glove.42B.300d.txt",
]
lib_paths = [data_dir + word_rep_dir + path for path in lib_paths]


########## Main working dataset
data_csv = data_dir + "data.csv"

# Name of combined word representation data_csv created by add_word_reps.py
combined_csv = data_dir + "data_combi.csv"

learning_data_dir = "learning_data/"   # Saved intermediate learning data

# Fields data types information
Y_labels_de = ['inc', 'dif', 'nrd', 'skt', 'vis', 'phy', 'obj', 'com']
# X_labels_de = ['x' + str(i) for i in range(300)]
X_labels_de = ["g42B_300d" + '_' + str(i) for i in range(300)]
X_labels_de = ["x" + str(n) for n in range(10 ** 3)] + \
    sum([[l + str(n) for n in range(10 ** 3)] for l in lib_names], [])

# Ngram counts - total and book count, year stats and recent counts
ngc_cols = ['ngc', 'nbc', 'mean', 'mean_mode', 'mode_mode',
            'min', 'max', 'last5', 'last10', 'last20']
gsc_col = 'gsc'             # Google search results count
X_labels_de += ngc_cols + [gsc_col]
labels_de = Y_labels_de + ngc_cols + [gsc_col]
Y_types = [bool, float, float, float, float, float, float, float]
n_stat = 3 # Number of x values suffixed to end of vector
n_def_labels = (len(labels_de) - n_stat)

# Key
l_key=" inc = 0/1 = whether word should be included at all in ideal game\n"+\
    " dif = Inverse difficulty\n" + \
    " nrd = Negative recognition difficulty = 10 - difficulty\n" + \
    " skt = Sketchability (ease of sketching in pictionary)\n" + \
    " vis = Visuality (visual nature)\n" + \
    " phy = Physicality (physical nature)\n" + \
    " obj = Objectness (whether or not it is an object)\n" + \
    " com = Commonality (well-known-ness among younger age groups)\n" + \
    " " + ngc_cols[0] + " = (Google) books corpus Ngram word count\n" + \
    " " + ngc_cols[1] + " = (Google) books corpus Ngram book count\n" + \
    " " + gsc_col     + " = Google search results count"


