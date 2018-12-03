import pandas as pd
import Utils.PathUtil as pu

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 50)
pd.set_option('max_colwidth', 100)


data = pd.read_csv(pu.flow_path)

comma = ","
data["city_district"] = data["city_code"] + comma + data["district_code"]

print(data["city_district"].drop_duplicates().tolist())