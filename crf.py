# -*- encoding=utf8 -*-
import numpy as np

TAGS = ["start", "stop"]


class Feature:

    def __init__(self):
        pass

    def __call__(self, y1, y2, x, i):
        return 1


test_feature = Feature()
Feature_table = [test_feature]


def compute_Mi(x, y, i, W):
    """
    计算输入x，位置i，标签y对应的矩阵Mi
    :param W: 特征方程参数矩阵
    :param x: 输入字符串
    :param y: 当前对应标签
    :param i: 当前输入下标
    :return: Mi矩阵
    """
    size = len(TAGS)
    Mi = np.zeros([size, size], dtype=np.float32)
    for i, y1 in enumerate(TAGS):
        for j, y2 in enumerate(TAGS):
            feature_sum = 0
            for k, feature in enumerate(Feature_table):
                feature_sum = feature_sum + W[k] * feature(y1, y2, x, i)
            Mi[i, j] = np.exp(feature_sum)
    return Mi


def compute_a(x, y, M):
    """
    前向（forward)动态规划计算所需的a向量组
    :param x:
    :param y:
    :param M:
    :return:
    """
    # 初始化a0, 对应的tag为start则为1，否则为0
    size = len(TAGS)
    a0 = np.zeros(size)
    a0[0] = 1

    a = [a0.copy()]

    # ai' = ai-1' * Mi
    for Mi in M:
        a0 = Mi.transpose().dot(a0)
        a.append(a0.copy())

    return a


def compute_b(x, y, M):
    """
    后向(backward)动态规划计算所需的a向量组
    :param x:
    :param y:
    :param M:
    :return:
    """
    # 初始化bn, 对应的tag为stop则为1，否则为0
    size = len(TAGS)
    bn = np.zeros(size)
    bn[-1] = 1

    b = [bn.copy()]

    for Mi in reversed(M):
        bn = Mi.dot(bn)
        b.append(bn.copy())

    return b[::-1]


if __name__ == "__main__":
    Mi = compute_Mi(None, None, 1, [1])
    a = compute_a(None, None, [Mi])
    b = compute_b(None, None, [Mi])

    print(a[0].dot(b[0].transpose())*Mi)
