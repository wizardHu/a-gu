# -*- encoding=utf8 -*-

import os
import csv
import datetime
directory = "/Users/game-netease/Documents/stock3"

WEEK = "week"
DAY = "day"

class a():
    pass


A = a()


def jdk_buy_week(kdjs, mas, datas, cur_index):
    j_low_0 = j连续5日低于0(kdjs, WEEK)
    j_to_0 = j多头行情超跌至0(kdjs, mas, datas, WEEK)
    kdj_golden_cross = False
    is_kdj_golden_cross = check_kdj_golden_cross(kdjs, WEEK)
    now_data = datas[WEEK][-1]
    # if is_kdj_golden_cross or j_low_0 or j_to_0:
    #     return True, "kdj"
    return False, ""


def jdk_buy_day(kdjs, mas, datas, cur_index):
    if ma_buy(mas, datas):
        return True, "ma"
    return False, ""

# 5 下穿20  盈利超过5 考虑卖
# 跌倒历史新低 并且当天超过6% 且触发止损 考虑等一等
# 近20日最高价 （需要高出一定幅度）不买 测试 或者  J 超过100并且近期最高考虑等一等再买
def ma_buy(mas, datas):
    p = DAY
    data = datas[p][-1]
    data_last_3 = datas[p][-3:]
    data_last_30_max = max([d["close"] for d in datas[p][-30:]])
    data_last_30_avg = sum([d["close"] for d in datas[p][-30:]])/len(datas[p][-30:])

    if mas.get(p) and len(mas[p].get("20", [])) > 3:
        last_5_3 = mas[p]["5"][-3:]
        last_20_3 = mas[p]["20"][-3:]
        for d in data_last_3:
            if d["amplitude"] > 0.07:
                return False
            # 长上引线 4 % 考虑不买
            low = max(d['close'], d['open'])
            if (d['high'] - low) / low > 0.04 and d['close']:
                return False
        if last_5_3[0] < last_20_3[0] and last_5_3[1] < last_20_3[1] and last_5_3[2] > last_20_3[2] and data['close'] > last_20_3[2]:
            if (last_5_3[2] - last_20_3[2]) / last_20_3[2] > 0.005:
                if data_last_30_max <= data['close'] and (data['close'] - data_last_30_avg) / data_last_30_avg >= 0.1:
                    return False
                return True
    return False


def judge_sell(kdjs, mas, datas, cur_index, position):
    can_sell = False
    p = DAY
    now_data = A.datas[DAY][-1]
    must_sell_price = position.get("must_sell", 0)
    reason = position.get("reason", "")
    r = ""

    last_5_3 = mas[p]["5"][-3:]
    last_20_3 = mas[p]["20"][-3:]

    if now_data["close"] < must_sell_price:
        can_sell = True
        r = "must_sell"
    if reason == "ma" and last_5_3[0] > last_20_3[0] and last_5_3[1] > last_20_3[1] and last_5_3[2] < last_20_3[2]:
        if now_data['close'] >= position["close"] and (now_data['close'] - position["close"]) / position["close"] > 0.02:
            can_sell = True
            r = "ma_low"
    return can_sell, r


def init_ma(data, period):
    last_60 = A.datas[period][-60:]
    last_20 = A.datas[period][-20:]
    last_10 = A.datas[period][-10:]
    last_5 = A.datas[period][-5:]

    if len(last_5) >= 5:
        avg = round(sum([d['close'] for d in last_5]) / 5, 2)
        A.ma.setdefault(period, {}).setdefault("5", []).append(avg)
        A.ma[period]["5"] = A.ma[period]["5"][-20:]

    if len(last_10) >= 10:
        avg = round(sum([d['close'] for d in last_10]) / 10, 2)
        A.ma.setdefault(period, {}).setdefault("10", []).append(avg)
        A.ma[period]["10"] = A.ma[period]["10"][-20:]

    if len(last_20) >= 20:
        avg = round(sum([d['close'] for d in last_20]) / 20, 2)
        A.ma.setdefault(period, {}).setdefault("20", []).append(avg)
        A.ma[period]["20"] = A.ma[period]["20"][-20:]

    if len(last_60) >= 60:
        avg = round(sum([d['close'] for d in last_60]) / 60, 2)
        A.ma.setdefault(period, {}).setdefault("60", []).append(avg)
        A.ma[period]["60"] = A.ma[period]["60"][-20:]


def init_kdj(data, period):
    Cn = data['close']
    Ln = 999999
    Hn = -999999
    if len(A.kdjs.get(period, [])) == 0:
        A.kdjs.setdefault(period, []).append({
            "k": 50,
            "d": 50,
            "j": 50,
            "date": data['date']
        })
        return
    for d in A.datas[period][-9:]:
        if d["high"] > Hn:
            Hn = d["high"]
        if d["low"] < Ln:
            Ln = d["low"]

    RSV = (Cn - Ln) / (Hn - Ln) * 100
    K = 2.0 / 3 * A.kdjs[period][-1]["k"] + 1.0 / 3 * RSV
    D = 2.0 / 3 * A.kdjs[period][-1]["d"] + 1.0 / 3 * K
    J = 3 * K - 2 * D

    A.kdjs[period].append({
        "k": round(K, 2),
        "d": round(D, 2),
        "j": round(J, 2),
        "date": data['date']
    })
    A.kdjs[period] = A.kdjs[period][-20:]


def j多头行情超跌至0(kdjs, ma, datas, period):
    now_j = kdjs[period][-1]["j"]
    if len(ma.get(period, {}).get("60", [])) < 15 or now_j > 0:
        return False
    last_15_60ma = ma[period]["60"][-15:]
    last_15_20ma = ma[period]["20"][-15:]
    last_15_10ma = ma[period]["10"][-15:]
    last_15_5ma = ma[period]["5"][-15:]

    for i in range(len(last_15_60ma)):
        if i == len(last_15_60ma) - 2:
            break
        if last_15_5ma[i] > last_15_10ma[i] > last_15_20ma[i] > last_15_60ma[i]:
            continue
        return False
    return True


def j连续5日低于0(kdjs, period):  # 50.8%
    last_5_j = [kdj["j"] for kdj in kdjs[period][-5:]]
    last_2_d = [kdj["d"] for kdj in kdjs[period][-2:]]
    if max(last_5_j) < 0 and max(last_2_d) < 20:
        return True
    return False


def check_kdj_golden_cross(kdj_data, period):
    if len(kdj_data[period]) < 3:
        return False
    today_kdj = kdj_data[period][-1]
    prev_kdj = kdj_data[period][-2]
    prev_2_kdj = kdj_data[period][-3]

    if today_kdj['k'] > today_kdj['d'] and prev_kdj['k'] < prev_kdj['d']:
        if prev_2_kdj['d'] - prev_2_kdj['k'] > 2.5\
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
    return p


def cal_range(row, next_row):
    c_close = row['close']
    n_close = next_row['close']
    diff = n_close - c_close
    return (diff / c_close) * 100


def init_data(row, period):
    A.datas.setdefault(period, []).append(row)
    A.datas[period] = A.datas[period][-60:]
    if len(A.datas[period]) > 1:
        A.datas[period][-1]["amplitude"] = (A.datas[period][-1]["close"] - A.datas[period][-2]["close"]) / A.datas[period][-2]["close"]


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
    data = [
        ['代码', '最终金额', '卖出次数', '买入次数', '胜利次数', '失败次数', '盈利金额', '亏损金额',
         '盈亏比', '最大持仓天数', '最小持仓天数', '平均持仓天数'],
    ]
    all_win = 0
    all_defeated = 0
    all_win_money = 0
    all_defeated_money = 0
    for filename in os.listdir(directory):
        A.kdjs = {}
        A.datas = {}
        A.ma = {}
        money = 100000
        position = []
        position_day = []
        buy_num = 0
        sell_num = 0
        win_num = 0
        defeated_num = 0
        win_money = 0
        defeated_money = 0

        # if "601128" not in filename:
        #     continue

        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='gbk') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # 跳过第一行
                column_index = {name: index for index, name in enumerate(header)}
                filtered_rows = [{
                    'code': filename.replace('.csv', ""),
                    'date': str(row[0]),
                    'open': float(row[column_index['open']]),
                    'high': float(row[column_index['high']]),
                    'low': float(row[column_index['low']]),
                    'close': float(row[column_index['close']]),
                } for row in csv_reader]
                if len(filtered_rows) == 0:
                    continue
                code = filtered_rows[0]["code"]
                # print("deal==", code)
                week_high = 0
                week_low = 9999
                week_open = filtered_rows[0]["open"]
                friday = False
                for i, row in enumerate(filtered_rows):
                    if row['open'] == 0:
                        continue
                    init_data(row, DAY)
                    init_kdj(row, DAY)
                    init_ma(row, DAY)
                    week_high = max(week_high, row['high'])
                    week_low = min(week_low, row['low'])
                    close = row['close']
                    can_sell_week = False
                    current_date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
                    if current_date.weekday() == 4:
                        weekly_row = {
                            'code': row['code'],
                            'date': row['date'],
                            'open': week_open,
                            'high': week_high,
                            'low': week_low,
                            'close': row['close']
                        }
                        week_open = 0
                        week_high = 0
                        week_low = 9999
                        init_data(weekly_row, WEEK)
                        init_kdj(weekly_row, WEEK)
                        init_ma(weekly_row, WEEK)
                        friday = True
                    else:
                        week_open = week_open if week_open != 0 else row['open']
                        friday = False
                    if i < 20:
                        continue
                    can_buy_week, reason = jdk_buy_week(A.kdjs, A.ma, A.datas, i)
                    can_buy_day, reason = jdk_buy_day(A.kdjs, A.ma, A.datas, i)
                    data_last_30_min = min([d["close"] for d in A.datas[DAY][-30:]])
                    if (friday and can_buy_week) or can_buy_day:
                        cost, hands = buy(money, row)
                        if hands > 0:
                            money = money - cost
                            row["hands"] = hands
                            row["buy_index"] = i
                            stop_loss = close * 0.9
                            stop_win = close * 1.1
                            last_20_min = min([r["low"] for r in filtered_rows[i-20: i]])
                            if (close - last_20_min) / close > 0.1:
                                stop_loss = last_20_min
                                stop_win = close + (close - last_20_min) * 1.2
                            elif i >= 40:
                                last_30_min = min([r["low"] for r in filtered_rows[max(0, i - 40): i]])
                                if (close - last_30_min) / close > 0.1:
                                    stop_loss = last_30_min
                                    stop_win = close + (close - last_30_min) * 1.2
                            if reason == "ma" and stop_loss < close * 0.9:
                                stop_loss = close * 0.9
                            row["stop_loss"] = round(stop_loss, 2)
                            row["stop_win"] = round(stop_win, 2)
                            row["reason"] = reason
                            row["max"] = close
                            position.append(row)
                            buy_num += 1
                    new_position = []
                    for p in position:
                        if p["date"] == row['date']:
                            new_position.append(p)
                            continue
                        p["max"] = p["max"] if p["max"] > close else close
                        can_sell, sell_reason = judge_sell(A.kdjs, A.ma, A.datas, i, p)
                        if row['close'] >= p["stop_win"]:
                            money += row['close'] * p["hands"] * 100
                            sell_num += 1
                            win_num += 1
                            win_money += ((row['close'] * p["hands"] - p["close"] * p["hands"]) * 100)
                            position_day.append(i - p["buy_index"])
                            print(code, close, row['date'], p["close"], p["date"], p["max"],
                                  round((p["max"] - p["close"]) / p["close"], 2) * 100,
                                  round((close - p["close"]) / p["close"], 2) * 100, "win")
                        elif row['close'] < p["stop_loss"] and data_last_30_min >= row['close'] and row['amplitude'] <= -0.06:
                            money += row['close'] * p["hands"] * 100
                            aa = row
                            sell_num += 1
                            defeated_num += 1
                            position_day.append(i - p["buy_index"])
                            defeated_money += ((p["close"] * p["hands"] - row['close'] * p["hands"]) * 100)
                            print(code, close,  row['date'], p["close"], p["date"], p["max"], round((p["max"]-p["close"])/p["close"], 2)*100,
                                  round((close - p["close"]) / p["close"], 2) * 100, "defeated")
                        elif can_sell:
                            if sell_reason == "ma_low":
                                money += row['close'] * p["hands"] * 100
                                sell_num += 1
                                win_num += 1
                                win_money += ((row['close'] * p["hands"] - p["close"] * p["hands"]) * 100)
                                position_day.append(i - p["buy_index"])
                                print(code, close, row['date'], p["close"], p["date"], p["max"],
                                      round((p["max"] - p["close"]) / p["close"], 2) * 100,
                                      round((close - p["close"]) / p["close"], 2) * 100, "win")

                            elif row['close'] >= p["close"]:
                                money += row['close'] * p["hands"] * 100
                                sell_num += 1
                                win_num += 1
                                win_money += ((row['close'] * p["hands"] - p["close"] * p["hands"]) * 100)
                                position_day.append(i - p["buy_index"])
                                print(code, close,  row['date'], p["close"], p["date"], p["max"],
                                      round((p["max"] - p["close"]) / p["close"], 2) * 100, round((close - p["close"]) / p["close"], 2) * 100, "win")
                            elif row['close'] < p["close"]:
                                money += row['close'] * p["hands"] * 100
                                aa = row
                                sell_num += 1
                                defeated_num += 1
                                position_day.append(i - p["buy_index"])
                                defeated_money += ((p["close"] * p["hands"] - row['close'] * p["hands"]) * 100)
                                print(code, close,  row['date'], p["close"], p["date"], p["max"],
                                      round((p["max"] - p["close"]) / p["close"], 2) * 100,
                                      round((close - p["close"]) / p["close"], 2) * 100, "defeated")
                        else:
                            if 0.05 <= round((p["max"]-p["close"])/p["close"], 2) < 0.1:
                                p["must_sell"] = p["close"] + p["close"] * 0.02
                            elif round((p["max"]-p["close"])/p["close"], 2) > 0.1:
                                p["must_sell"] = p["close"] + p["close"] * 0.05
                            if round((p["max"]-p["close"])/p["close"], 2) > 0.15:
                                p["must_sell"] = p["close"] + p["close"] * 0.1
                            new_position.append(p)
                    position = new_position

                    if i == len(filtered_rows) - 1:
                        for p in position:
                            if close >= p["close"]:
                                money += close * p["hands"] * 100
                                sell_num += 1
                                win_num += 1
                                win_money += ((close * p["hands"] - p["close"] * p["hands"]) * 100)
                                position_day.append(i - p["buy_index"])
                                print(code, close, row['date'], p["close"], p["date"], p["max"],
                                      round((p["max"] - p["close"]) / p["close"], 2) * 100,
                                      round((close - p["close"]) / p["close"], 2) * 100, "win")
                            elif close < p["close"]:
                                money += close * p["hands"] * 100
                                sell_num += 1
                                defeated_num += 1
                                defeated_money += ((p["close"] * p["hands"] - close * p["hands"]) * 100)
                                position_day.append(i - p["buy_index"])
                                print(code, close, row['date'], p["close"], p["date"], p["max"],
                                      round((p["max"] - p["close"]) / p["close"], 2) * 100,
                                      round((close - p["close"]) / p["close"], 2) * 100, "defeated")

        # data = [
        #     ['代码', '初始金额', '最终金额', '交易次数', '卖出次数', '买入次数', '胜利次数', '失败次数', '盈利金额', '亏损金额',
        #      '盈亏比', '最大持仓天数', '最小持仓天数', '平均持仓天数'],
        # ]
        data.append([
            code, money, sell_num, buy_num, win_num, defeated_num, win_money, defeated_money,
            round(win_money/defeated_money, 2) if defeated_money > 0 else 1,
            max(position_day) if position_day else 0,
            min(position_day) if position_day else 0,
            int(sum(position_day)/len(position_day) if position_day else 0)
        ])
        all_defeated += defeated_num
        all_defeated_money += defeated_money
        all_win += win_num
        all_win_money += win_money
        #break
    with open("./result.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        # 写入数据
        writer.writerows(data)

    print(f"all_win={all_win}, all_defeated={all_defeated},win_defeated_gap={all_win-all_defeated} ,win_defeated={all_win/all_defeated},"
          f" all_win_money={all_win_money}, all_defeated_money={all_defeated_money}, money_gap={all_win_money-all_defeated_money}")
