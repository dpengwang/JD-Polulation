import time
import  datetime
import pandas as pd
import Utils.PathUtil as pu
from dateutil.parser import parse
import Utils.FeatureUtil as fu
import Utils.CommonUtil as cu
import pickle
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 2000)
pd.set_option('max_colwidth',100)
pd.set_option("display.width",1000)


class PreProcess:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        comma = ","
        self.data["date_dt"] = self.data["date_dt"].apply(lambda x: self.formate_date(x))
        if list(self.data.columns) == fu.origin_flow_feature:
            self.data["aim_city_district"] = self.data["city_code"] + comma + self.data["district_code"]
            return self.data[fu.processed_flow_feature]
        else:
            self.data["o_city_district"] = self.data["o_city_code"] + comma + self.data["o_district_code"]
            self.data["d_city_district"] = self.data["d_city_code"] + comma + self.data["d_district_code"]
            return self.data[fu.processed_transition_feature]

    def formate_date(self, date):
        a = str(parse(str(date))).split(" ")[0]
        b = time.strptime(a, "%Y-%m-%d")
        c = time.strftime("%Y-%m-%d", b)
        return c

class Process_Transition:

    def __init__(self,data):
        self.data =data

    def process(self):
        self.data1 = pd.pivot_table(self.data, index=["date_dt", "o_city_district"], columns=["d_city_district"],
                           values=["cnt"]).reset_index(inplace=False)
        self.data2 = pd.pivot_table(self.data, index=["date_dt", "d_city_district"], columns=["o_city_district"],
                                   values=["cnt"]).reset_index(inplace=False)
        self.data1.columns = self.change_columns(list(self.data1.columns), "flowTo")
        self.data2.columns = self.change_columns(list(self.data2.columns), "flowFrom")
        res = pd.merge(self.data1, self.data2)
        return res

    def change_columns(self,columns, flag):
        columns[1] = "aim_city_district"
        for i in range(len(columns)):
            if i == 1: continue
            columns[i] = "".join(columns[i])
            columns[i] = columns[i].replace("cnt", flag)
        return columns


class Method1:

    def complent_flow_data(self):

        data = pd.read_csv(pu.origin_flow_path)
        data["date_dt"] = data["date_dt"].apply(lambda x: "{0}-{1}-{2}".format(str(x)[:4], str(x)[4:6], str(x)[6:]))
        date = cu.getDayDate("2018-03-02", -30)
        print(date)

        datalist = cu.getDateListFromWindow(date,15)

        newdata = data[data["date_dt"].isin(datalist)]
        for fea in fu.predict_feature:
            newdata[fea] = 0

        newdata['date_dt'] = newdata["date_dt"].apply(lambda x: cu.getDayDate(x, 32))
        res = pd.concat([data,newdata],axis=0).reset_index(inplace=False)
        # print(res)
        res.to_csv(pu.origin_root_path + "flow_train.csv",index=None)


    def genMergeData(self):
        flow_data = PreProcess(pd.read_csv(pu.origin_flow_path)).process_data()
        transiction_data = PreProcess(pd.read_csv(pu.origin_transition_path)).process_data()
        transiction_data = Process_Transition(transiction_data).process()

        flow_data.to_csv(pu.processed_root_path + "flow.csv", index=None)
        transiction_data.to_csv(pu.processed_root_path + "transiction.csv", index=None)

        merge_data = pd.merge(flow_data,transiction_data)
        merge_data.to_csv(pu.merge_data_path, index=None)


    def genTrainTestData(self,windowSize):
        data = pd.read_csv(pu.processed_root_path + "merge.csv")
        labeldata = pd.read_csv(pu.processed_root_path + "flow.csv")

        res = pd.DataFrame()

        for windowStartDate in cu.getDateListFromEndDate(fu.start_date, cu.getDayDate(fu.end_date, -1*(windowSize+15))):
            print("batch of {0} is generating".format(windowStartDate))
            currentDateBatch = cu.getDateListFromWindow(windowStartDate, windowSize)
            windowEndDate = cu.getDayDate(windowStartDate, windowSize)

            #统计特征部分
            data0 = data[data["date_dt"].isin(currentDateBatch)]
            data0['weekday'] = data0["date_dt"].apply(lambda x: cu.getWeekDay(x))
            # data0["flagDate"] = windowStartDate
            countFeature = list(data0.columns)
            countFeature.remove("date_dt")

            # data1 = data0[countFeature].groupby(["aim_city_district"]).agg(['min', 'mean', 'max',"std"]).reset_index(inplace=False)
            # data1.columns = map(lambda x:changeColumnName(x),list(data1.columns))


            # print(data0[fu.predict_feature+""].columns)
            data2 = data0[fu.predict_feature+["aim_city_district", "weekday"]].groupby(["aim_city_district", "weekday"]).agg(['min', 'mean', 'max',"std"]).reset_index(inplace=False)
            data2.columns = map(lambda x:self.changeColumnName(x,flag="ByWeekDay", specialword=["aim_city_district","weekday"]), list(data2.columns))


            data2 =pd.pivot_table(data2, index=["aim_city_district"], columns=["weekday"],
                           ).reset_index(inplace=False)
            data2.columns = map(lambda x:self.changeColumnName(x, specialword=["aim_city_district"]), list(data2.columns))


            # print(list(data1.columns))
            # print(list(data2.columns))
            # print(data1.shape)
            # print(data2.shape)

            datam = data2



            datam["flagDate"] = windowStartDate
            datam["duration"] = windowStartDate + "~" + windowEndDate

            labelDateList = cu.getDateListFromWindow(cu.getDayDate(windowEndDate, 1), 15)
            labelData = labeldata[labeldata["date_dt"].isin(labelDateList)]
            mergeData = pd.merge(datam, labelData)

            mergeData["preDay"] = mergeData[["flagDate", "date_dt"]].apply(lambda x: cu.getDateDistance(x[1], x[0], windowSize), axis=1)
            mergeData.rename(columns={'date_dt': 'predictDate'}, inplace=True)

            res = pd.concat([res, mergeData], axis=0)
            # res.to_csv("D:/qq.csv")
            # break

        res["specialDay"] = res["predictDate"].apply(lambda x: cu.getSpecialDay(x))
        res["weekday"] = res["predictDate"].apply(lambda x: cu.getWeekDay(x))


        trainFlagDateList = cu.getDateListFromEndDate(fu.start_date, cu.getDayDate(fu.train_end_date, -1*(windowSize+15)))
        testFlagDate = cu.getDayDate(fu.end_date, -1*(windowSize+15))

        # print(trainFlagDateList)
        # print(testFlagDate)

        trainData = res[res["flagDate"].isin(trainFlagDateList)]
        testData  = res[res["flagDate"] == testFlagDate]

        # testData["preDay"] = testData[["flagDate"]].apply(lambda x: cu.getDateDistance("2018-03-16", x[0], windowSize), axis=1)

        trainData.to_csv(pu.train_test_data_root_path + "{0}_train.csv".format(windowSize), index=None)
        testData.to_csv(pu.train_test_data_root_path + "{0}_test.csv".format(windowSize), index=None)



    def changeColumnName(x, flag="", specialword=[""]):
        if len(flag)==0:
          return x[0] + x[1] if len(x) > 1 else x
        else:

            if len(x) == 1:
                if x in specialword:
                    res = x
                else:
                    res = x + flag
            else:
                if x[0] not in specialword and x[1] not in specialword:
                    res = x[0] + x[1] + flag
                else:
                    res = x[0] + x[1]

            return res

class Method2:
    def save_obj(self, obj, name):
        with open(pu.map_root_path + name + ".pkl", "wb") as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


    def load_obj(self, name):
        with open(pu.map_root_path + name + ".pkl", "rb") as f:
            return pickle.load(f)

    def genMap(self,feature):
        data = pd.read_csv(pu.origin_flow_path)
        fea_data = data[feature].drop_duplicates().values
        print(len(fea_data))
        map = {}
        for i in range(len(fea_data)):
            map[fea_data[i]] = i+1
        self.save_obj(map,feature)

    def genTest(self):
        datelist = cu.getDateListFromWindow("2018-03-02",15)
        citylist  = pd.read_csv(pu.origin_root_path + "flow_train.csv")[["city_code","district_code"]].drop_duplicates().values

        array = []
        for date in datelist:
            for city in citylist:
                array.append(np.concatenate([np.array([date]),city], axis=0))
        test_data = pd.DataFrame(array,columns=["date_dt","city_code","district_code"])
        for fea in fu.predict_feature:
            test_data[fea] = 0

        test_data.to_csv(pu.train_test_data_root_path + "new_data.csv",index=None)

    def ExtractFeature(self,data):
        cityMap = self.load_obj("city_code")
        districtMap = self.load_obj("district_code")
        data["city"] = data["city_code"].apply(lambda x: cityMap[x])
        data["district"] = data["district_code"].apply(lambda x: districtMap[x])
        data["weekDay"] = data["date_dt"].apply(lambda x: cu.getWeekDay(x))
        data["month"] = data["date_dt"].apply(lambda x: cu.getMonth(x))
        data["countryHoliDay"] = data["date_dt"].apply(lambda x: cu.getCountryHoliDay(x))
        data["springDay"] = data["date_dt"].apply(lambda x: cu.getSpringDay(x))
        data["monthDay"] = data["date_dt"].apply(lambda x: cu.getMonthDay(x))
        data["monthPerid"] = data["date_dt"].apply(lambda x: cu.getMonthPeriod(x))
        data["weekOfMonth"] = data["date_dt"].apply(lambda x: cu.getWeekofMonth(x))
        data["quarter"]  = data["date_dt"].apply(lambda x: cu.getQuarter(x))
        data["weekofyear"]  = data["date_dt"].apply(lambda x: cu.getWeekofYear(x))
        data["summerva"]  = data["date_dt"].apply(lambda x: cu.getSumvocation(x))


        data["monthhalf"] = data["date_dt"].apply(lambda x: cu.getMonthHalf(x))


        calc =["mean"] #
        groupedWeekDay= data[["weekDay","city_code", "district_code"]+fu.predict_feature].groupby(["city_code", "district_code","weekDay"]).agg(calc).reset_index()
        groupedMonth= data[["month","city_code", "district_code"]+fu.predict_feature].groupby(["city_code", "district_code","month"]).agg(calc).reset_index()
        groupedMonthDay= data[["monthDay","city_code", "district_code"]+fu.predict_feature].groupby(["city_code", "district_code","monthDay"]).agg(calc).reset_index()

        groupedWeekDay.columns = cu.changeColumnsNames("ByWeekDay",list(groupedWeekDay.columns))
        groupedMonth.columns = cu.changeColumnsNames("ByMonth",list(groupedMonth.columns))
        groupedMonthDay.columns = cu.changeColumnsNames("ByMonthDay",list(groupedMonthDay.columns))
        #
        res = pd.merge(groupedWeekDay,data)
        res = pd.merge(res,groupedMonth)
        res = pd.merge(res,groupedMonthDay)
        # #
        city_mean = data[["city_code"] + fu.predict_feature].groupby(["city_code"]).mean().reset_index()
        discrict_mean = data[["district_code"] + fu.predict_feature].groupby(["district_code"]).mean().reset_index()

        city_mean["city_rank"] = (city_mean["flow_in"] + city_mean["flow_out"]).apply(lambda x: int(x // 98))
        discrict_mean["district_rank"] = (discrict_mean["flow_in"] + discrict_mean["flow_out"]).apply(lambda x: int(x // 98))

        city_rank = city_mean[["city_code", "city_rank"]]
        district_rank = discrict_mean[["district_code", "district_rank"]]
        #
        district_in_city = data[["district_code","city_code"]].drop_duplicates().groupby(["city_code"]).count().reset_index()
        district_in_city.columns = ["city_code","district_in_city"]
        # #
        res = pd.merge(res, city_rank)
        res = pd.merge(res, district_rank)
        res = pd.merge(res, district_in_city)
        #
        features = list(data.columns)
        drop_features = ["city_code", "district_code", "city", "district", "date_dt"] + fu.predict_feature
        for fea in drop_features:
            if fea in features:
                features.remove(fea)

        poly_transformer = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        poly_data = pd.DataFrame(poly_transformer.fit_transform(data[features]),
                                 columns=poly_transformer.get_feature_names(features))
        data = pd.concat([res, poly_data], join="inner", axis=1)

        columns = self.delFeatures(list(data.columns))
        data =data[columns]
        print(columns)

        return data
        # return res

    def delFeatures(self,columns):
        timeFea = ["month", "countryHoliDay","monthDay", "weekDay","monthPerid", "quarter","weekOfMonth" ]
        for fea in columns:
            if " " in fea:
                fea1 = fea.split(" ")[0]
                fea2 = fea.split(" ")[1]
                if (fea1 not in timeFea and fea2 not in timeFea): #or (fea1  in timeFea and fea2  in timeFea):
                    columns.remove(fea)

        return columns



    def genTranTest(self):
        origin_train = pd.read_csv(pu.origin_root_path + "flow_train.csv")
        origin_test = pd.read_csv(pu.train_test_data_root_path + "new_data.csv")

        self.ExtractFeature(origin_train).to_csv(pu.train_test_data_root_path +'train.csv',index=None)
        self.ExtractFeature(origin_test).to_csv(pu.train_test_data_root_path +'test.csv', index=None)
        print("finish")

a = Method2()
a.genTest()
a.genTranTest()
# a.genCityInfo()

# print(data)





















