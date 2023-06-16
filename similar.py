import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(kdj1, kdj2):
    similarities = []
    for i in range(3):  # 对每个K、D、J分别计算相似度
        similarity = cosine_similarity(kdj1[:, i].reshape(1, -1), kdj2[:, i].reshape(1, -1))
        similarities.append(similarity[0][0])
    return similarities

def find_similar_kdj(kdj_set, kdj, threshold):
    similar_kdj = None

    for kdj_data in kdj_set:
        similarities = calculate_cosine_similarity(kdj_data, kdj)
        if all(similarity >= threshold for similarity in similarities):
            similar_kdj = kdj_data
            break

    return similar_kdj

# 示例数据
N = 100  # 集合中KDJ数据的数量
kdj_set = np.random.rand(N, 16, 3)  # 集合中的KDJ数据，假设为N组连续16天的KDJ，每组KDJ有3个值：K、D、J
kdj = np.random.rand(16, 3)  # 给定的一组连续16天的KDJ，包含K、D、J三个值
threshold = 0.9  # 相似度阈值

similar_kdj = find_similar_kdj(kdj_set, kdj, threshold)
if similar_kdj is not None:
    print("kdj:")
    print(kdj)
    print("与给定KDJ最相似的组合:")
    print(similar_kdj)
else:
    print("没有找到满足相似度要求的KDJ")
