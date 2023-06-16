# -*- encoding=utf8 -*-

import os
import csv
from datetime import datetime

directory = "/Users/game-netease/Documents/stock"


class a():
    pass


A = a()


def jdk_buy(kdjs, mas, datas, cur_index):
    j_low_0 = j连续5日低于0(kdjs)
    j_to_0 = j多头行情超跌至0(kdjs, mas, datas)
    kdj_golden_cross = False
    is_kdj_golden_cross = check_kdj_golden_cross(kdjs)
    now_data = datas[-1]
    if is_kdj_golden_cross:
        return True
    return False


def init_ma(data):
    last_60 = A.datas[-60:]
    last_20 = A.datas[-20:]
    last_10 = A.datas[-10:]
    last_5 = A.datas[-5:]

    if len(last_5) >= 5:
        avg = round(sum([d['close'] for d in last_5]) / 5, 2)
        A.ma.setdefault("5", []).append(avg)
        A.ma["5"] = A.ma["5"][-20:]

    if len(last_10) >= 10:
        avg = round(sum([d['close'] for d in last_10]) / 10, 2)
        A.ma.setdefault("10", []).append(avg)
        A.ma["10"] = A.ma["10"][-20:]

    if len(last_20) >= 20:
        avg = round(sum([d['close'] for d in last_20]) / 20, 2)
        A.ma.setdefault("20", []).append(avg)
        A.ma["20"] = A.ma["20"][-20:]

    if len(last_60) >= 60:
        avg = round(sum([d['close'] for d in last_60]) / 60, 2)
        A.ma.setdefault("60", []).append(avg)
        A.ma["60"] = A.ma["60"][-20:]


def init_kdj(data):
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


def j多头行情超跌至0(kdjs, ma, datas):
    now_j = kdjs[-1]["j"]
    if len(ma.get("60", [])) < 15 or now_j > 0:
        return False
    last_15_60ma = ma["60"][-15:]
    last_15_20ma = ma["20"][-15:]
    last_15_10ma = ma["10"][-15:]
    last_15_5ma = ma["5"][-15:]

    for i in range(len(last_15_60ma)):
        if i == len(last_15_60ma) - 2:
            break
        if last_15_5ma[i] > last_15_10ma[i] > last_15_20ma[i] > last_15_60ma[i]:
            continue
        return False
    return True


def j连续5日低于0(kdjs):  # 50.8%
    last_5_j = [kdj["j"] for kdj in kdjs[-5:]]
    last_2_d = [kdj["d"] for kdj in kdjs[-2:]]
    if max(last_5_j) < 0 and max(last_2_d) < 20:
        return True
    return False


def check_kdj_golden_cross(kdj_data):
    today_kdj = kdj_data[-1]
    prev_kdj = kdj_data[-2]
    prev_2_kdj = kdj_data[-3]

    if today_kdj['k'] > today_kdj['d'] and prev_kdj['k'] < prev_kdj['d']:
        if prev_2_kdj['d'] - prev_2_kdj['k'] > 4\
                and today_kdj['k'] - today_kdj['d'] > 1.5:
            p1 = Point(1, prev_kdj['k'])
            p2 = Point(2, today_kdj['k'])
            line1 = Line(p1, p2)

            p3 = Point(1, prev_kdj['d'])
            p4 = Point(2, today_kdj['d'])
            line2 = Line(p3, p4)
            pointXY = GetCrossPoint(line1, line2)

            return pointXY.y <= 20
    return False


class Point():
    x = 0
    y = 0

    # 定义构造方法
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def GetLinePara(line):
    line.a = line.p1.y - line.p2.y;
    line.b = line.p2.x - line.p1.x;
    line.c = line.p1.x * line.p2.y - line.p2.x * line.p1.y;


def GetCrossPoint(l1, l2):
    GetLinePara(l1);
    GetLinePara(l2);
    d = l1.a * l2.b - l2.a * l1.b
    p = Point()
    p.x = (l1.b * l2.c - l2.b * l1.c) * 1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a) * 1.0 / d
    return p;


def cal_range(row, next_row):
    c_close = row['close']
    n_close = next_row['close']
    diff = n_close - c_close
    return (diff / c_close) * 100


def init_data(row):
    A.datas.append(row)
    A.datas = A.datas[-60:]


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
    buy_num = 0
    sell_num = 0
    win_num = 0
    defeated_num = 0
    win_money = 0
    defeated_money = 0
    money_sum = 0


    for filename in os.listdir(directory):
        A.kdjs = []
        A.datas = []
        A.ma = {}
        A.last_kdj_cross = {}
        money = 100000
        money_sum += money
        position = []
        # if "300413" not in filename:
        #     continue

        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='gbk') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # 跳过第一行
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
                # print("deal==", code)
                for i, row in enumerate(filtered_rows):
                    init_data(row)
                    init_kdj(row)
                    init_ma(row)
                    sold = False
                    if i < 21:
                        continue
                    close = row['close']
                    if jdk_buy(A.kdjs, A.ma, A.datas, i):
                        cost, hands = buy(money, row)
                        if hands > 0:
                            money = money - cost
                            row["hands"] = hands
                            stop_loss = close * 0.95
                            stop_win = close * 1.1
                            last_20_min = min([r["close"] for r in filtered_rows[i-20: i]])
                            if (close - last_20_min) / close > 0.03:
                                stop_loss = last_20_min
                                stop_win = close + (close - last_20_min) * 1.2
                            else:
                                last_30_min = min([r["close"] for r in filtered_rows[max(0, i - 30): i]])
                                if (close - last_30_min) / close > 0.03:
                                    stop_loss = last_30_min
                                    stop_win = close + (close - last_30_min) * 1.2
                            row["stop_loss"] = round(stop_loss, 2)
                            row["stop_win"] = round(stop_win, 2)
                            position.append(row)
                            buy_num += 1
                    new_position = []
                    for p in position:
                        if close >= p["stop_win"]:
                            money += close * p["hands"] * 100
                            sell_num += 1
                            win_num += 1
                            win_money += ((close * p["hands"] - p["close"] * p["hands"]) * 100)
                        elif close < p["stop_loss"]:
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
       # break

    print(f" money_sum={money_sum}, buy_num={buy_num}, win_num={win_num},"
          f" win_money={win_money}, sell_num={sell_num}, defeated_num={defeated_num}, defeated_money={defeated_money}")
