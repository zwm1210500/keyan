import numpy as np
import math


def cal_len(vec):
    vec = np.mat(vec)
    num = (float)(vec * vec.T)
    return math.sqrt(num)

def norm(vec):
    vec = np.array(vec)
    return vec / cal_len(vec)


a = np.mat([1, 1, 1])

b = norm(a)

print(b)

