import pandas as pd
import Utils.PathUtil as pu
import Utils.FeatureUtil as fu
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 50)
pd.set_option('max_colwidth',100)
pd.set_option("display.width",1000)



window = 45

res = pd.DataFrame().empty
pathtp = pu.predict_root_path + "{0}.csv"

dwell = pd.read_csv(pathtp.format("dwell"))
flowin = pd.read_csv(pathtp.format("flow_in"))
flowout = pd.read_csv(pathtp.format("flow_out"))


a = pd.merge(dwell,flowin)
b = pd.merge(a,flowout)



# b['dwell'] =b['dwell'].apply(lambda x:abs(x))
# b['flow_in'] =b['flow_in'].apply(lambda x:abs(x))
# b['flow_out'] =b['flow_out'].apply(lambda x:abs(x))
#
# b["city"] = b["city_district"].apply(lambda x:x.split(",")[0])
# b["district"] = b["city_district"].apply(lambda x:x.split(",")[1])
# res =b.drop(["city_district"], axis=1)
# res["predictDate"] = res["predictDate"].apply(lambda x:x.replace("-",""))
# res =res[['predictDate',"city",'district',"dwell","flow_in","flow_out"]]


b = b.sort_values(["city_code", "district_code", "date_dt"], inplace=False)

for fea in fu.predict_feature:
    b[fea] = b[fea].apply(lambda x: 0 if x < 0 else x)

b.to_csv(pu.predict_root_path + 'prediction.csv',index=None,header=0)

print(b)