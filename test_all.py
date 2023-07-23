import math

def calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4):
    vector1 = (x2 - x1, y2 - y1)
    vector2 = (x4 - x3, y4 - y3)

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    norm1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    norm2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    cosine = dot_product / (norm1 * norm2)
    angle = math.acos(cosine)

    return math.degrees(angle)

# 示例数据
x1, y1 = 0, 44
x2, y2 = 1, 51
x3, y3 = 0, 48
x4, y4 = 1, 46

result = calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4)
print(f"两条线段之间的夹角为：{result} 度")
