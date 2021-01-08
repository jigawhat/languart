# Refresh google search results count for each word in the dataset

from Constants import *
from Dataset import *

ds = Dataset(data_csv, labels_de)
ds.load()
ds.refresh_gsearch_counts()
ds.save()

