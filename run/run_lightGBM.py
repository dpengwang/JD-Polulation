from threading import Thread

import pandas as pd
import lightgbm as lgb
import Utils.PathUtil as pu
import Utils.FeatureUtil as fu
import matplotlib.pyplot as plt
import matplotlib
from sklearn.externals import joblib
import threading
import Utils.CommonUtil as cu
from sklearn.model_selection import train_test_split

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
matplotlib.use('qt4agg')

def run(predict_feature):
    print(predict_feature)

    params = {
        "objective": "regression",
        "metric": "rmse",
        "num_leaves": 80,
        "min_child_samples": 60,
        "learning_rate": 0.3,
        "feature_fraction": 0.8,
        "bagging_frequency": 1,
        "bagging_seed": 666,
        "reg_lambda": 20,
        "verbosity": -1
    }

    # train_date_list = cu.getDateListFromEndDate(fu.start_date, "2017-12-01")
    # valid_date_list = cu.getDateListFromEndDate("2017-12-16", "2017-12-31")
    # valid_date = "2017-12-31"
    # timeWindow = "45"
    #
    # train_data = pd.read_csv(pu.train_test_data_root_path + "{0}_train.csv".format(timeWindow))
    # test_data = pd.read_csv(pu.train_test_data_root_path + "{0}_test.csv".format(timeWindow))
    #
    #
    # origin_train_data = train_data[train_data["flagDate"].isin(train_date_list)]
    # origin_valid_data = train_data[train_data["flagDate"].isin(valid_date_list)]
    #
    # nouse_feature = fu.nouse_feature_for_train
    # for fea in nouse_feature:
    #      if fea == predict_feature:
    #              nouse_feature.remove(fea)
    #
    # train_data = origin_train_data.drop(nouse_feature, axis=1)
    # valid_data = origin_valid_data.drop(nouse_feature, axis=1)
    #
    # train_features = list(train_data.columns)
    # train_features.remove(predict_feature)
    #
    # X_train = train_data[train_features]
    # Y_train = train_data[predict_feature]
    #
    # X_val = valid_data[train_features]
    # Y_val = valid_data[predict_feature]
    #
    # lgb_train = lgb.Dataset(X_train, Y_train)
    # lgb_eval = lgb.Dataset(X_val, Y_val, reference=lgb_train)
    #
    # gbm = lgb.train( params,
    #                  lgb_train,
    #                  num_boost_round=40000,
    #                  valid_sets=lgb_eval,
    #                  early_stopping_rounds=100,
    #                  verbose_eval=100
    #                 )
    #
    #
    # valid_predict_data = origin_valid_data.reset_index(inplace=False)
    # valid_predict_label = pd.DataFrame(gbm.predict(X_val, num_iteration=gbm.best_iteration),
    #                                    columns=["predict_" + predict_feature])
    # valid_predict_data = pd.concat([valid_predict_data, valid_predict_label], axis=1)
    # city_district_name = fu.city_district_name[2]
    #
    # origin = valid_predict_data[valid_predict_data["aim_city_district"] == city_district_name][predict_feature].values
    # predict = valid_predict_data[valid_predict_data["aim_city_district"] == city_district_name]["predict_" + predict_feature].values
    #
    # axis = [i for i in range(1, len(origin)+1)]
    # plt.plot(axis, origin, color="blue", label="origin")
    # plt.plot(axis, predict, color="green", label=predict_feature)
    # plt.legend()
    # plt.show()
    #
    #
    # #预测结果
    # test_id = test_data[['predictDate', "aim_city_district"]]
    # predict_data = gbm.predict(test_data[train_features], num_iteration=gbm.best_iteration)
    # predict_data = pd.DataFrame(predict_data, columns=["predict" + predict_feature])
    # res = pd.concat([test_id, predict_data], axis=1)
    # res.columns=["predicyDate","city_district","predict"]
    #

    #
    # joblib.dump(gbm,pu.model_path + "{0}_{1}.pkl".format(predict_feature, timeWindow))

    cityCode ="06d86ef037e4bd311b94467c3320ff38"
    districtCode = "85792b2278de59316d1158f6a97537ec"


    train_data = pd.read_csv(pu.train_test_data_root_path + "train.csv")
    test_data = pd.read_csv(pu.train_test_data_root_path + "test.csv")
    # date_dt, city_code, district_code, dwell, flow_in, flow_out, cityFea, districtFea, weekDayFea, monthFea, specialDayFea

    train_feature = list(train_data.columns)
    nouse_fea = ["city_code","district_code"] + fu.predict_feature  #, "date_dt"
    for fea in nouse_fea:
        if fea in train_feature:
            train_feature.remove(fea)

    print(predict_feature in train_feature, train_feature)

    # return

    # X = train_data[train_feature]
    # Y = train_data[predict_feature]

    train, val = train_test_split(train_data, test_size=0.3, random_state=55)

    X_train = train[train_feature]
    Y_train = train[predict_feature]

    X_val = val[train_feature]
    Y_val = val[predict_feature]




    lgb_train = lgb.Dataset(X_train, Y_train)
    lgb_eval = lgb.Dataset(X_val, Y_val, reference=lgb_train)

    gbm = lgb.train( params,
                     lgb_train,
                     num_boost_round=40000,
                     valid_sets=[lgb_train, lgb_eval],
                     early_stopping_rounds=100,
                     verbose_eval=100
                    )


    districtName = val["district_code"].values[0]
    showData = val[val["district_code"] == districtName]

    valid_y = gbm.predict(showData[train_feature], num_iteration=gbm.best_iteration)

    axis = [i for i in range(len(valid_y))]
    plt.plot(axis, valid_y, color="blue", label="predict")
    plt.plot(axis, showData[predict_feature], color="green", label="origin")
    plt.legend()
    plt.show()


    test_id = test_data[["date_dt", "city_code", "district_code"]]
    pre_y = gbm.predict(test_data[train_feature], num_iteration=gbm.best_iteration)

    pre_y = pd.DataFrame(pre_y, columns=[predict_feature])
    res = pd.concat([test_id,pre_y], axis=1)
    res.to_csv(pu.predict_root_path + "{0}.csv".format(predict_feature), index=None)




for fea in fu.predict_feature:
    run(fea)





