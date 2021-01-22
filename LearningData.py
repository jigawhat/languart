

#
#  Learning data utilitions
#

import joblib
from collections import defaultdict

from Constants import *
from Utils import *
from Dataset import *
from DataRequests import *
from WordRepLibrary import *


def load_data(Y_labels=Y_labels_de, X_labels=X_labels_de, data=data_csv):
    dataset = Wordset(data)
    df = dataset.load()
    X_labels = [l for l in X_labels if l in df.columns]
    return df, np.array(df[X_labels]), np.array(df[Y_labels])


def save_ld(data, name, pad=True, compress=False):
    if pad:
        create_folder(data_dir + learning_data_dir)
        name = data_dir + learning_data_dir + name + ".data"
    joblib.dump(data, name, compress=compress)

def load_ld(name, pad=True):
    if pad: name = os.path.join(data_dir, learning_data_dir, name + ".data")
    return joblib.load(name)
