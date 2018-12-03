import datetime
import Utils.FeatureUtil as fu

def getDayDate(date,n):
    #获得指定日期的前后n天
    if "-" not in str(date):
        date = "{0}-{1}-{2}".format(str(date)[:4], str(date)[4:6], str(date)[6:])
    date = date.split("-")
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2])) + datetime.timedelta(days=n)
    date = date.strftime('%Y-%m-%d')
    return date

def getCountryHoliDay(date):
    #判断是否为特殊的日子
    date = str(date)


    if date in fu.countryHoliDay:
        return 1
    else:
        return 0

def getWeekDay(date):
    if "-" not in str(date):
        date = "{0}-{1}-{2}".format(str(date)[:4], str(date)[4:6], str(date)[6:])
    date = date.split("-")
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    date = date.strftime("%w")
    if date =="0": return "7"
    return date


def getDateListFromWindow(startDate,window):
    #获得从从startDate开始往后window天的日期 包括startDate
    if "-" not in startDate:
        startDate = "{0}-{1}-{2}".format(str(startDate)[:4], str(startDate)[4:6], str(startDate)[6:])

    endDate = getDayDate(startDate, window)
    date_list = []
    begin_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y%m%d")

        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def getDateListFromEndDate(startDate,endDate):
    startDate = str(startDate)
    endDate = str(endDate)
    if "-" not in startDate:
        startDate = "{0}-{1}-{2}".format(startDate[:4], startDate[4:6], startDate[6:])
    if "-" not in endDate:
        endDate = "{0}-{1}-{2}".format(endDate[:4], endDate[4:6], endDate[6:])
    date_list = []
    begin_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

def getDateDistance(endDate,startDate,windowSize):
    startDate = str(startDate)
    endDate = str(endDate)
    if "-" not in startDate:
        startDate = "{0}-{1}-{2}".format(startDate[:4], startDate[4:6], startDate[6:])
    if "-" not in endDate:
        endDate = "{0}-{1}-{2}".format(endDate[:4], endDate[4:6], endDate[6:])

    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    count = 0
    while startDate <= endDate:
        # date_str = begin_date.strftime("%Y-%m-%d")
        count += 1
        startDate += datetime.timedelta(days=1)
    return count -windowSize - 1

def getMonth(date):
    date =str(date)
    if "-" in date:
        return int(date.split("-")[1])
    else:
        return int(date[4:6])

def getMonthDay(date):
    date =str(date)

    if "-" in date:
        return int(date.split("-")[2])
    else:
        return int(date[6:8])

def changeColumnsNames(flag,columns):
    for i in range(len(columns)):
       if columns[i][1] == "":
          columns[i] = columns[i][0] + columns[i][1]
       else:
          columns[i] = columns[i][0] + columns[i][1] + "_" + flag

    return columns

def getMonthPeriod(date):
    date =  int(str(date)[6:])
    if date <= 10:
        return 1
    elif date >20:
        return 2
    else:
        return 3
def getSpringDay(date):
    date = str(date)
    if date in fu.springDay:
        return 1
    else:
        return 0


def getWeekofMonth(date):
    date =str(date)
    end = int(datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:])).strftime("%W"))
    begin = int(datetime.datetime(int(date[:4]), int(date[4:6]), 1).strftime("%W"))
    return end - begin + 1


def getQuarter(date):
    date = int(str(date)[4:6])
    return (date +1) //3


# date ="20170501"
# a = getMonthPeriod(date)
# print(getMonthPeriod(date))
# print(getMonth(date))
# print(getSpecialDay(date))
# print(getWeekDay(date))
# print(getDateListFromWindow("20180101",10))
# print(getSpringDay("20180501"))
