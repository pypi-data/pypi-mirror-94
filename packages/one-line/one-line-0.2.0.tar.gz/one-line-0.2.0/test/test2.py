from oneline import OneData
from oneline import io
import pandas as pd
from time import time

start = time()
a = OneData('test/Mall_Customers.csv')
train, test = a.make_dataset(train_frac=0.7, random=True)
print(type(train), type(test))
end = time()
print(end - start)
