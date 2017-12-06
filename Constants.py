#
#   Constants.py
#
# Shared constants for project
#


######## Data folder
data_dir = "data/"


######## Google Ngram counts data
ngrams_dir = "ngrams/"
ngrams_data = data_dir + ngrams_dir + "google_20120701_1grams/"
ngrams_counts = data_dir + "ngram_counts.csv"
ngrams_count_period = [2000, 2020]   # (Inclusive)


########### Main word representation library
word_rep_dir = "word_reps/"
word_rep_data = data_dir + word_rep_dir + "glove.6B/glove.6B.300d.txt"

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

# Fields data types information
# X_labels_default = ['x' + str(i) for i in range(300)]
X_labels_default = ["g42B_300d" + '_' + str(i) for i in range(300)]
Y_labels_default = ['inc', 'dif', 'nrd', 'skt', 'vis', 'phy', 'obj', 'com']
ngc_cols = ['ngc', 'nbc']   # Ngram counts - total and book count
gsc_col = 'gsc'             # Google search results count
X_labels_default += ngc_cols + [gsc_col]
labels_default = Y_labels_default + ngc_cols + [gsc_col]
Y_types = [bool, float, float, float, float, float, float, float]
n_stat = 3 # Number of x values suffixed to end of vector
n_def_labels = (len(labels_default) - n_stat)

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


