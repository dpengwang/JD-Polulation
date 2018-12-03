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


# data = pd.read_csv(pu.processded_root_path +'train.csv')[["flagDate","date_dt"]].to_csv(pu.processed_root_path + "new_data.csv",index=None)


# res = []
# res += cu.getDateListFromWindow("20170430",3)
# res += cu.getDateListFromWindow("20171001",7)
# res += cu.getDateListFromWindow("20170530",3)
# res += cu.getDateListFromWindow("20180101",3)


print(cu.getDateListFromEndDate("20180210","20180222"))


# print(a)