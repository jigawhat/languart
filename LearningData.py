

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


def load_data(Y_labels=Y_labels_de, X_labels=X_labels_de, data=combined_csv):
    dataset = Dataset(data)
    df = dataset.load()
    X_labels = [l for l in X_labels if l in df.columns]
    return df, np.array(df[X_labels]), np.array(df[Y_labels])


def save_learning_data(data, name):
    create_folder(data_dir + learning_data_dir)
    joblib.dump(data, data_dir + learning_data_dir + name + ".data")
    
def load_learning_data(name):
    return joblib.load(data_dir + learning_data_dir + name + ".data")
