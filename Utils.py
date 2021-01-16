'''
    
    Utility methods

'''

import os
import gc
import sys
import shutil
import pprint
import traceback
from collections import OrderedDict
import pandas as pd


# Return the first index of a substring s
def strind(w, s):
    try:
        return w.index(s)
    except:
        return None

# Default word root algorithm
def word_root(s):
    return s.lower().replace('-', '')

# Return the head of a string split by separator sep
def strh(s, sep):
    return s[:strind(s, sep)]

# Return whether x is within range r
def within(x, r):
    return r[0] <= x <= r[1]

# Get the current time as a timestamp
def get_curr_ts():
    return pd.Timestamp.now().timestamp()

# Print an exception's usual output, formatted correctly
def pr_exception(e):
    for line in traceback.format_tb(e.__traceback__):
        sys_print(line)
    sys_print(type(e))
    sys_print(e)

# Print directly using standard output
def sys_print(obj):
    sys.stdout.write(str(obj))
    sys.stdout.flush()

# Print dictionaries (etc) in a human readable way
pp = pprint.PrettyPrinter(indent=4)
def pr(obj):
    pp.pprint(obj)

# Format an iterable of numbers for printing
def fm_nums(iterable, round_n):
    return [float("{:,}".format(round(n, round_n))) for n in iterable]

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


