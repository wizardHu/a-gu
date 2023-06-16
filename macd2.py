import numpy as np

emaArray={}

def calculateEMA(data, period):
    multiplier = 2 / (period + 1)  # EMA的平滑系数
    if not emaArray.get(f"{period}"):
        emaArray[f"{period}"] = [data]
        return emaArray[f"{period}"][0]
    now_ema = (data - emaArray[f"{period}"][-1]) * multiplier + emaArray[f"{period}"][-1]
    emaArray[f"{period}"] = emaArray[f"{period}"].append(now_ema)
    return now_ema


#计算MACD的值
def calculateMACD(data,shortPeriod = 12 ,longPeriod = 26 ,signalPeriod =9):
    ema12 = calculateEMA(data['close'],shortPeriod)
    ema26 = calculateEMA(data['close'],longPeriod)
    diff = ema12-ema26
    dea= calculateEMA(diff, signalPeriod)
    macd = 2*(diff-dea)
    return macd,diff,dea

# 示例数据
kline_data = [
{'close':40.8},
{'close':52.43}
]

for k in kline_data:
    macd,diff,dea = calculateMACD(k )
    print("DIF:", diff)
    print("DEA:", dea)
    print("MACD:", macd)
