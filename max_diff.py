import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
"""统计16周期内，j 值最大与最小的差值"""
filename = 'j.csv'  # 替换为你的 CSV 文件名
differences = []

with open(filename, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        values = [float(value) for value in row]  # 将每个值转换为浮点数
        max_value = max(values)
        min_value = min(values)
        difference = max_value - min_value
        differences.append(round(difference, 2))

data = np.array(differences)
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
