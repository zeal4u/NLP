# -*- encoding=utf8 -*-
import networkx as nx


class Transducer:
    FINAL = 0
    START = 1
    NORMAL = 2

    def __init__(self):
        self.start_node = None
        self.graph = None

    def next(self, node):
        result = []
        for key, value in self.graph.adj[node].items():
            result.append((value["char"], key))
        return result

    def type(self, node):
        return self.graph.nodes[node]['type']

    def save(self, path):
        if isinstance(self.graph, nx.DiGraph):
            nx.write_gml(self.graph, path)

    @staticmethod
    def load(file_path):
        graph = nx.read_gml(file_path)
        transducer = Transducer()
        transducer.graph = graph
        transducer.start_node = ""
        return transducer

    @staticmethod
    def construct(words):
        graph = nx.DiGraph()

        start_node = ""
        graph.add_node(start_node, type=Transducer.START)

        next_node = ""
        for word in words:
            cur_node = ""
            for char in word:
                for key, value in graph.adj[cur_node].items():
                    if value['char'] == char:
                        cur_node = key
                        break
                else:
                    # 不存在char相应的边就生成新的边
                    next_node = cur_node + char
                    graph.add_edge(cur_node, next_node, char=char)
                    graph.nodes[next_node]['type'] = Transducer.NORMAL
                    cur_node = next_node
            else:
                graph.nodes[next_node]['type'] = Transducer.FINAL

        transducer = Transducer()
        transducer.start_node = start_node
        transducer.graph = graph
        transducer.save("test.tdr")

        return transducer


def ed(a, i, b, j, H):
    """
    计算字符串 a 和 b之间的 edit distance
    :param a:
    :param i: len of curr a
    :param b:
    :param j: len of curr b
    :param H: matrix stores ed between a[:i] and b[:j]
    :return: ed between a[:i] and b[:j]
    """
    if i == 0:
        return j
    if j == 0:
        return i
    if H[i - 1][j - 1] != -1:
        # already computed a[:i+1] and b[:j+1]
        return H[i - 1][j - 1]
    if a[i - 1] == b[j - 1]:
        result = ed(a, i - 1, b, j - 1, H)
    elif i >= 2 and j >= 2 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
        # last two characters are transposed
        result = 1 + min(ed(a, i - 2, b, j - 2, H), ed(a, i, b, j - 1, H), ed(a, i - 1, b, j, H))
    else:
        result = 1 + min(ed(a, i - 1, b, j - 1, H), ed(a, i, b, j - 1, H), ed(a, i - 1, b, j, H))
    H[i - 1][j - 1] = result
    return result


def cuted(origin, candidate, t):
    m = len(origin)
    n = len(candidate)
    l = max(1, n - t)
    u = min(m, n + t)
    min_ed = n
    H = [[-1 for _ in range(n)] for _ in range(m)]
    for i in range(l, u + 1):
        new_ed = ed(origin, i, candidate, n, H)
        if min_ed > new_ed:
            min_ed = new_ed
    return min_ed


def spell_correction(origin, t, tdr):
    """
    纠正输入的英文单词，返回候选正确形式
    :param origin: 待纠正单词
    :param t: 最大edit distance
    :param tdr: 语言自动机网络
    :return:
    """
    start_node = tdr.start_node
    candidates = [start_node]
    result = []
    while candidates:
        cur_word = candidates.pop(-1)
        for char, next_word in tdr.next(cur_word):
            if cuted(origin, next_word, t) <= t:
                # 在语言自动机里，FINAL state也可以有后续状态（一个单词可能只是另一个单词的前缀）
                candidates.append(next_word)

                if transducer.type(next_word) == tdr.FINAL:
                    # 达到一个FINAL state，找到了一个单词
                    H = [[-1 for _ in range(len(next_word))] for _ in range(len(origin))]
                    if ed(origin, len(origin), next_word, len(next_word), H) <= t:
                        result.append(next_word)

    return result


if __name__ == "__main__":
    transducer = Transducer.load("test.tdr")
    words = ["ab", "cv", "ac", "stff", "wnderful"]
    for next_word in words:
        print(spell_correction(next_word, 2, transducer))
