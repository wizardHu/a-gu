# -*- encoding=utf8 -*-

import os
import csv
from datetime import datetime
directory = "/Users/game-netease/Documents/stock"
class a():
    pass

A = a()

def calculateEMA(data, period):
    multiplier = 2 / (period + 1)  # EMA的平滑系数
    if not A.emaArray.get(f"{period}"):
        A.emaArray[f"{period}"] = [data]
        return A.emaArray[f"{period}"][0]
    now_ema = (data - A.emaArray[f"{period}"][-1]) * multiplier + A.emaArray[f"{period}"][-1]
    A.emaArray[f"{period}"].append(now_ema)
    return now_ema

#计算MACD的值
def calculateMACD(data,shortPeriod = 12 ,longPeriod = 26 ,signalPeriod =9):
    ema12 = calculateEMA(data['close'],shortPeriod)
    ema26 = calculateEMA(data['close'],longPeriod)
    diff = ema12-ema26
    dea= calculateEMA(diff, signalPeriod)
    macd = 2*(diff-dea)
    return macd,diff,dea



if __name__ == "__main__":
    all_j = []
    for filename in os.listdir(directory):
        A.emaArray = {}
        A.datas = []
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='gbk') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # 跳过第一行
                min_data = []
                kdj_list = []
                cutoff_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
                filtered_rows = [{
                        'code': row[0],
                        'date': str(row[2]),
                        'open': float(row[3]),
                        'high': float(row[4]),
                        'low': float(row[5]),
                        'close': float(row[6]),
                    } for row in csv_reader if datetime.strptime(row[2], '%Y-%m-%d') > cutoff_date]
                if len(filtered_rows) == 0:
                    continue

                for i, row in enumerate(filtered_rows):
                    print(calculateMACD(row))
        break