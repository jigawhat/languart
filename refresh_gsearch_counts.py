# Refresh google search results count for each word in the dataset

from Constants import *
from Dataset import *

ds = Wordset()
ds.load()
ds.refresh_gsearch_counts()
ds.save()

