

import os
import glob
from Utils import *
from Constants import *



### Rename files

os.chdir(ngrams_data)
files = glob.glob("googlebooks-eng-*")

for f in files:
    os.rename(f, f.split('-')[-1])


