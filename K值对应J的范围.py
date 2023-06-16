# -*- encoding=utf8 -*-

import os
import csv
from datetime import datetime
directory = "/Users/game-netease/Documents/stock"
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
class a():
    pass

A = a()


def init_kdj(data):
    A.datas.append(data)
    A.datas = A.datas[-20:]
    Cn = data['close']
    Ln = 999999
    Hn = -999999
    if len(A.kdjs) == 0:
        A.kdjs.append({
            "k": 50,
            "d": 50,
            "j": 50,
            "date": data['date']
        })
        return
    for d in A.datas[-9:]:
        if d["high"] > Hn:
            Hn = d["high"]
        if d["low"] < Ln:
            Ln = d["low"]

    RSV = (Cn - Ln) / (Hn - Ln) * 100
    K = 2.0 / 3 * A.kdjs[-1]["k"] + 1.0 / 3 * RSV
    D = 2.0 / 3 * A.kdjs[-1]["d"] + 1.0 / 3 * K
    J = 3 * K - 2 * D

    A.kdjs.append({
        "k": round(K, 2),
        "d": round(D, 2),
        "j": round(J, 2),
        "date": data['date']
    })
   # A.kdjs = A.kdjs[-3:]


if __name__ == "__main__":
    all_j = []
    for filename in os.listdir(directory):
        A.kdjs = []
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
                print("deal==", filtered_rows[0]["code"])
                for row in filtered_rows:
                    init_kdj(row)
                for i, row in enumerate(filtered_rows):
                    close = row['close']
                    min_close = min(
                        row['close'] for row in filtered_rows[max(0, i - 15):min(i + 16, len(filtered_rows))])

                    if close == min_close:
                        min_data.append(row)
                        kdj_list.append(A.kdjs[max(0, i - 15):min(i + 1, len(A.kdjs))])
                #print(kdj_list)
                for kdjs in kdj_list:
                    padding_dict = {
                        "k": 50,
                        "d": 50,
                        "j": 50
                    }
                    while len(kdjs) < 16:
                        kdjs.insert(0, padding_dict)
                    for index in [6]:
                        kdj = kdjs[15 - index]
                        if kdj['k'] >= 10 and kdj['k'] <= 45:
                            all_j.append(kdj['j'])
                #break
    #print(all_j)
    data = np.array(all_j)
    # 绘制直方图
    plt.hist(data, bins=50, density=True, alpha=0.5)

    # 绘制核密度估计图
    kde = gaussian_kde(data)
    x = np.linspace(min(data), max(data), 100)
    plt.plot(x, kde(x), 'r')

    # 设置图形属性
    plt.title('Distribution of Data')
    plt.xlabel('Value')
    plt.ylabel('Density')

    # 显示图形
    plt.show()