# -*- encoding=utf8 -*-

import os
import csv
from datetime import datetime
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
    A.kdjs = A.kdjs[-20:]


def jdk_buy(kdjs, data):
    last_5_j = [kdj["j"] for kdj in kdjs[-5:]]
    last_2_d = [kdj["d"] for kdj in kdjs[-2:]]
    if max(last_5_j) < 0 and max(last_2_d) < 20:
        return True
    return False


def buy(money, row):
    space = 10
    cost = money / space
    close = row["close"]
    hands = int(cost/(close * 100))
    while hands == 0 and space > 1:
        space = space - 1
        cost = money / space
        hands = int(cost / (close * 100))
    return close * 100 * hands, hands


if __name__ == "__main__":
    for filename in os.listdir(directory):
        A.kdjs = []
        A.datas = []
        position = []
        money = 100000
        buy_num = 0
        sell_num = 0
        win_num = 0
        defeated_num = 0
        win_money = 0
        defeated_money = 0
        code = ""
        if "300413" not in filename:
            continue

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
                code = filtered_rows[0]["code"]
                #print("deal==", code)
                for i, row in enumerate(filtered_rows):
                    init_kdj(row)
                    if i < 16:
                        continue
                    close = row['close']
                    # 注意这里算上了今日的收盘价
                    last_15_min_close = min([r["close"] for r in filtered_rows[i - 15: i + 1]])

                    if jdk_buy(A.kdjs, row):
                        print(last_15_min_close, row['date'], row['code'])
                        cost, hands = buy(money, row)
                        if hands > 0:
                            money = money - cost
                            row["hands"] = hands
                            position.append(row)
                            buy_num += 1

                    new_position = []
                    for p in position:
                        if close >= p["close"] * 1.05:
                            money += close * p["hands"] * 100
                            sell_num += 1
                            win_num += 1
                            win_money += ((close * p["hands"] - p["close"] * p["hands"]) * 100)
                        elif close < p["close"] * 0.95:
                            money += close * p["hands"] * 100
                            sell_num += 1
                            defeated_num += 1
                            defeated_money += ((p["close"] * p["hands"] - close * p["hands"]) * 100)
                        else:
                            new_position.append(p)
                    position = new_position

                    if i == len(filtered_rows) - 1:
                        for p in position:
                            if close >= p["close"]:
                                money += close * p["hands"] * 100
                                sell_num += 1
                                win_num += 1
                                win_money += ((close * p["hands"] - p["close"] * p["hands"]) * 100)
                            elif close < p["close"]:
                                money += close * p["hands"] * 100
                                sell_num += 1
                                defeated_num += 1
                                defeated_money += ((p["close"] * p["hands"] - close * p["hands"]) * 100)

        print(f"code={code}, money={money}, buy_num={buy_num}, win_num={win_num},"
              f" win_money={win_money}, sell_num={sell_num}, defeated_num={defeated_num}, defeated_money={defeated_money}")
        #break
