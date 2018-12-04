import time
from dateutil.parser import parse
import Utils.PathUtil as pu
import Utils.CommonUtil as cu
import pandas as pd
import numpy as np
import  datetime
import Utils.FeatureUtil as fu

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 50)
pd.set_option('max_colwidth',100)
pd.set_option("display.width",1000)


data = pd.read_csv(pu.train_test_data_root_path + "train.csv")
corr =data.corr()
print(corr)




# print(a)