import pandas as pd


# 读取csv文件
df = pd.read_csv('k.csv')

for i in range(16):
    print(f'{i+1}', " ===="*8)
    # 获取指定列的数据
    numbers = df[f'{i+1}']

    # 定义范围区间和区间数量
    ranges = [(0, 10), (10, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
    range_counts = [0] * len(ranges)

    # 遍历数字数组并计算每个数字所属的范围
    for number in numbers:
        for i, (start, end) in enumerate(ranges):
            if start <= number < end:
                range_counts[i] += 1
                break

    # 输出每个范围的数量
    for i, (start, end) in enumerate(ranges):
        print(f"{start}-{end}: {range_counts[i]}")