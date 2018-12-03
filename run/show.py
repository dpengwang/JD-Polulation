import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import Utils.PathUtil as pu
import Utils.FeatureUtil as fu
import matplotlib.dates as mdates
import Utils.CommonUtil as cu



plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
matplotlib.use('qt4agg')




data = pd.read_csv(pu.origin_root_path + "flow_train.csv")
cityCode ="06d86ef037e4bd311b94467c3320ff38"
districtCode = "85792b2278de59316d1158f6a97537ec"
data = data[(data["city_code"] == cityCode) & (data["district_code"] == districtCode)]
print(data.shape)
dwell = data["dwell"].values
flow_in = data["flow_in"].values
flow_out = data["flow_out"].values
#
#
#  # 自动旋转日期标记
#
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 50)
pd.set_option('max_colwidth',100)
pd.set_option("display.width",1000)
data["date_dt"] = data["date_dt"].apply(lambda x:str(cu.getMonthPeriod(x)))

# axis = list(map(lambda x:str(x),data["date_dt"].values))
axis  =list(data["date_dt"].values)
print(axis)
plt.plot(axis, dwell, color="blue", label ="dwell")
# plt.plot(axis, flow_in , color="green", label ="flow_in")
# plt.plot(axis, flow_out, color="red", label ="flow_out")

plt.legend()

plt.show()


# city_mean = data[["city_code"]+fu.predict_feature].groupby(["city_code"]).mean().reset_index()
# discrict_mean = data[["district_code"]+fu.predict_feature].groupby(["district_code"]).mean().reset_index()
#
# city_mean["city_rank"] = (city_mean["flow_in"] + city_mean["flow_out"]).apply(lambda x: int(x//98))
# discrict_mean["district_rank"] = (discrict_mean["flow_in"] + discrict_mean["flow_out"]).apply(lambda x: int(x//98))
#
# city_rank = city_mean[["city_code","city_rank"]]
# district_rank = discrict_mean[["district_code","district_rank"]]
#
# # print(district_rank)
# data = pd.read_csv(pu.origin_root_path + "transition_train.csv")
# data = data[(data["date_dt"]==20170603)&(data["o_district_code"] == "879c99a1536ce81df8e84c0c9cf6ff68") & (data["o_city_code"]=="a20d041605db832309e26c003c626719")]
# label = data["cnt"].values
# axis =  data["d_district_code"].values
#
# plt.plot(axis, label ,color ="green", label="cnt")
# plt.legend()
# plt.show()






# print(b)