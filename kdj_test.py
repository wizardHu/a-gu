# -*- encoding=utf8 -*-

import os
import csv

directory = "/Users/game-netease/Documents/stock"


class a():
    pass


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
    line.a =line.p1.y - line.p2.y;
    line.b = line.p2.x - line.p1.x;
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y;


def GetCrossPoint(l1,l2):

    GetLinePara(l1);
    GetLinePara(l2);
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p;

A = a()


def judgeJDKBuy():
    KDJModelList = A.kdjs

    if len(KDJModelList) < 3:
        return False

    thisModel = KDJModelList[-1]
    lastModel = KDJModelList[-2]

    K = thisModel['k']
    D = thisModel['d']
    J = thisModel['j']

    lastK = lastModel['k']
    lastD = lastModel['d']
    lastJ = lastModel['j']
    isBuy = False

    if K < D and lastK > lastD and D - K > 1 and lastK - lastD > 1:  # 普通下穿
        p1 = Point(1, lastK)
        p2 = Point(2, K)
        line1 = Line(p1, p2)

        p3 = Point(1, lastD)
        p4 = Point(2, D)
        line2 = Line(p3, p4)

        pointXY = GetCrossPoint(line1, line2)
        if pointXY.y < 60:
            isBuy = True

    if KDJModelList[-3]['j'] < 0 and lastJ < 0 and J < 0:
            isBuy = True

    if K>55 and D>55 or abs(J-lastJ)<30:
        isBuy = False

    return isBuy


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
        "k": K,
        "d": D,
        "j": J,
    })
    A.kdjs = A.kdjs[-3:]


if __name__ == "__main__":
    A.kdjs = []
    A.datas = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='gbk') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # 跳过第一行
                for row in csv_reader:
                    data = {
                        'code': row[0],
                        'date': row[2],
                        'open': float(row[3]),
                        'high': float(row[4]),
                        'low': float(row[5]),
                        'close': float(row[6]),
                    }
                    init_kdj(data)
                    if judgeJDKBuy():
                        print(data)
