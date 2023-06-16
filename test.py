import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

import pandas as pd

# 读取csv文件
df = pd.read_csv('k.csv')

for i in range(16):
    # 获取指定列的数据
    data = df[f'{i+1}'].to_numpy()

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

