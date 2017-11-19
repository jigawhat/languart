#
# remove_dataset_rows.py
#
#


import pandas as pd
from Constants import *


rows_to_remove = [ 'sktb', 'visb', 'phyb', 'objb', 'comb', ]


df = pd.read_csv(data_csv, index_col=0)
df = df[[col for col in list(df.columns) if col not in rows_to_remove]]
# print(df)
df.to_csv(data_csv)


