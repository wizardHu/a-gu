# -*- encoding=utf8 -*-

import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
directory = "/Users/game-netease/Documents/stock"

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


def draw(kdj_list):
    for item in kdj_list:
        dates = []
        ks = []
        ds = []
        js = []

        for i in item:
            dates.append(i['date'])
            ks.append(i['k'])
            ds.append(i['d'])
            js.append(i['j'])

        plt.plot(dates, ks, label='K')
        plt.plot(dates, ds, label='D')
        plt.plot(dates, js, label='J')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('KDJ')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    all_k = {}
    all_d = {}
    all_j = {}
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
                #print(min_data)
                #print(kdj_list)
                for kdjs in kdj_list:
                    padding_dict = {
                        "k": 50,
                        "d": 50,
                        "j": 50
                    }
                    while len(kdjs) < 16:
                        kdjs.insert(0, padding_dict)
                    for i, kdj in enumerate(kdjs):
                        all_k.setdefault(f"{16-i}", []).append(kdj["k"])
                        all_d.setdefault(f"{16 - i}", []).append(kdj["d"])
                        all_j.setdefault(f"{16 - i}", []).append(kdj["j"])

                draw(kdj_list)

                break
    # data = {"sheet_k":all_k, "sheet_d":all_d, "sheet_j":all_j}
    # print(data)
    # writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    #
    # # Iterate over the sheets in the data dictionary
    # for sheet_name, sheet_data in data.items():
    #     # Create a DataFrame from the sheet data
    #     df = pd.DataFrame(sheet_data)
    #
    #     # Write the DataFrame to the Excel file
    #     df.to_excel(writer, sheet_name=sheet_name, index=False)
    #
    # # Save the Excel file
    # writer.save()