#
#   Constants.py
#
# Shared constants for project
#


data_dir = "data/"
data_csv = data_dir + "data.csv"

word_rep_data = data_dir + "word_reps/glove.6B/glove.6B.300d.txt"
# word_rep_data = data_dir + "word_reps/glove.6B/glove.6B.50d.txt"
# word_rep_data = data_dir + "word_reps/glove.42B.300d/glove.42B.300d.txt"

ngrams_data = data_dir + "ngrams/google_20120701_1grams/"
ngrams_counts = data_dir + "ngram_counts.csv"

ngrams_count_period = [2000, 2020]   # (Inclusive)


# Fields data types information

labels_default = \
    ['val', 'dif', 'nrd', 'skt', 'vis', 'phy',
     'obj', 'com', 'ngc', 'nbc', 'gsc']

Y_types = [bool, float, float, float, float, float, float, float]
n_stat = 3 # Number of x values suffixed to end of vector
n_y = (len(labels_default) - n_stat)

# Key
l_key=" val = 0 or 1 -> whether it is a valid english word to see in-game\n"+\
    " dif = Inverse difficulty\n" + \
    " nrd = Negative recognition difficulty = 10 - difficulty\n" + \
    " skt = Sketchability (ease of sketching in pictionary)\n" + \
    " vis = Visuality (visual nature)\n" + \
    " phy = Physicality (physical nature)\n" + \
    " obj = Objectness (whether or not it is an object)\n" + \
    " com = Commonality (well-known-ness among younger age groups)\n" + \
    " ngc = (Google) books corpus Ngram word count\n" + \
    " nbc = (Google) books corpus Ngram book count\n" + \
    " gsc = Google search results count"


