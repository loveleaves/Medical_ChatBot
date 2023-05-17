import jieba
import numpy
import math


class CosinSimilarity:
    """
    function: 两个文本余弦相似度计算
    """

    def get_similarity(self, s1: str, s2: str, retain_acc=3) -> float:
        """
        function: 获取两个文本之间的余弦相似度
        params:
            s1: 文本1
            s2: 文本2
        return:
            相似度
        """
        list_1, list_2 = self.divide_sent(s1, s2)
        all_words = self.get_all_words(list_1, list_2)
        vec1, vec2 = self.get_word_vector(list_1, list_2, all_words)
        cos_score = self.calculate_cos(vec1, vec2)
        return round(cos_score, retain_acc)

    def divide_sent(self, a: str, b: str):
        """
        function: 分词
        """
        a1 = jieba.cut(a)
        b1 = jieba.cut(b)
        list_a = []
        list_b = []
        for i in a1:
            list_a.append(i)
        for j in b1:
            list_b.append(j)
        return list_a, list_b

    def get_all_words(self, list_a: str, list_b: str):
        """
        function: 获取所有的分词
        """
        all_words = []
        for i in list_a:
            if (i not in all_words):
                all_words.append(i)
        for j in list_b:
            if (j not in all_words):
                all_words.append(j)
        return all_words

    def get_word_vector(self, list_a, list_b, all_words):
        """
        function: 词频向量化
        """
        la = []
        lb = []
        for word in all_words:
            la.append(list_a.count(word))
            lb.append(list_b.count(word))
        return la, lb

    def calculate_cos(self, vec1, vec2):
        """
        function: 计算余弦值
        """
        laa = numpy.array(vec1)
        lbb = numpy.array(vec2)
        cos = (numpy.dot(laa, lbb.T)) / ((math.sqrt(numpy.dot(laa, laa.T))) * (math.sqrt(numpy.dot(lbb, lbb.T))))
        return cos


if __name__ == '__main__':
    compute_cos = CosinSimilarity()
    print(compute_cos.get_similarity("这个病传染性很强", "高传染性疾病"))