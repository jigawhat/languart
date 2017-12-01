'''
    
    Utility methods

'''

import os
import sys
import shutil
import pprint
from collections import OrderedDict
import pandas as pd


# Return whether x is within range r
def within(x, r):
    return r[0] <= x <= r[1]

# Print directly using standard output
def sys_print(obj):
    sys.stdout.write(str(obj))
    sys.stdout.flush()

# Print dictionaries (etc) in a human readable way
pp = pprint.PrettyPrinter(indent=4)
def pr(obj):
    pp.pprint(obj)

# Create folder, optionally overwriting existing folder
def create_folder(path, overwrite=False):
    if(os.path.isdir(path)):
        if(overwrite):
            shutil.rmtree(path)
        else:
            return
    os.mkdir(path)


# Utility data functions

def df_add(df, X, index):
    Y = [OrderedDict(x) for x in X]
    if df is None:
        df = pd.DataFrame(Y, index=index)
    else:
        df.loc[index] = [y.values() for y in Y]
    return df

def save_json(obj, name):
    with open(data_dir + name + '.json', 'w') as outfile:
        json.dump(obj, outfile)

def load_json(name):
    with open(data_dir + name + '.json', 'r') as infile:
        return json.load(infile)


