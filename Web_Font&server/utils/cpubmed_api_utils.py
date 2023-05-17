# -*- coding:utf-8 -*-
import requests
import json

class CpubMedApi:
    """
    function : 利用HIT CPubMed-KG处理数据
    Official Website : https://cpubmed.openi.org.cn/graphwiki/api
    """
    def __init__(self):
        self.sign_id = "#" #  your sign_id
        self.api_base_url = "https://cpubmedgraph.cn/graph/"

    def get_entity_schema(self, entity: str):
        """
        function : 获取实体相关三元组
        return : {'影像学检查': [['双源CT检查', '7159040'],], '发病性别倾向': [['XXX', '146587']], ...}
        """
        api_url = self.api_base_url + "schema?"
        params = {"entity": entity, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)[entity]
            return data
        except:
            return None

    def get_triple_info(self, triple_id: str):
        """
        function : 获取三元组信息
        return : {
                "triple_id": "14529",
                "doc_id": "46790947,22917575,...",
                "text": "糖尿病大鼠血管平滑肌细胞内质网应激因子GRP78和caspase12的表达及阿托伐他汀的干预作用",
                "doc_num": 198,
                "doctitle": ["糖尿病大鼠血管平滑肌细...", "阿托伐他汀对2型糖尿病鼠...", ...]
            }
        """
        api_url = self.api_base_url + "triple-info?"
        params = {"ID": triple_id, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except:
            return None

    def get_word_cut(self, sent: str):
        """
        function : 分词
        return :
            [
                ["肝癌", "疾病"],
                ["的", "停用词"],
                ["发生", "停用词"],
                ["是", "停用词"],
                ...
            ]
        """
        api_url = self.api_base_url + "cut?"
        params = {"query": sent, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except:
            return None

    def get_match_triple(self, sent):
        """
        function : 三元组匹配
        return : 即 [三元组id，头实体，关系，尾实体]
            [
                ["8024214", "肝癌", "高危因素", "抑郁程度高"],
                ["62505", "肝癌", "高危因素", "年龄"],
                ["8928743", "肝癌", "高危因素", "合并高血压"],
                ["12505", "肝癌", "高危因素", "糖尿病"],
                ...
            ]
        """
        api_url = self.api_base_url + "match?"
        params = {"query": sent, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except:
            return None

    def retrieve_paper(self, sent):
        """
        function : 医学文献检索
        return : 其中[docid: str, title: str, keywords: list, abstract: str]
        [
            {
                "f_ID": "13262879",
                "f_Title": "晚期肝癌介入置管埋泵化疗的常见并发症及护理对策",
                "f_keyword": "肝癌%介入%置管%化疗泵%护理",
                "f_Abstract": "回顾性分析30例晚期肝癌患者施,娴熟的注射...",
            },
            {
                ,,,
            },
            ...
        ]
        """
        api_url = self.api_base_url + "retrieve?"
        params = {"query": sent, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except:
            return None

    def get_triple_path(self, source_entity: str, target_entity: str):
        """
        function : 查找实体间三元组路径
        return : 其中 [路径1，路径2，路径3,...]
            [
                [
                    ["心脏病",相关（导致）,心律失常],[心律失常,高危因素,"糖尿病"]
                ],
                [
                    ["心脏病",病理分型,主动脉夹层],[主动脉夹层,病因,"糖尿病"]
                ],
                [
                    ["心脏病",病因,感染],[感染,高危因素,"糖尿病"]
                ],
                ...
            ]
        """
        api_url = self.api_base_url + "path?"
        params = {"source-entity": source_entity, "target-entity": target_entity, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except Exception as e:
            print(e)
            return None

    def get_entity_similarity(self, entity1: str, entity2: str):
        """
        function : 计算实体相似度
        return : 距离越小，相似度越大，距离最小为0
        """
        api_url = self.api_base_url + "similarity?"
        params = {"ent1": entity1, "ent2": entity2, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            score = res.text
            return score
        except:
            return None

    def get_similar_entity(self, entity: str):
        """
        function : 获取相近的实体词
        return :  	[实体1，实体2，...]
        """
        api_url = self.api_base_url + "similar-entity?"
        params = {"entity": entity, "sign": self.sign_id}
        try:
            res = requests.get(api_url, params=params)
            data = json.loads(res.text)
            return data
        except:
            return None

if __name__ == "__main__":
    api = CpubMedApi()
    entity = "其他关节病"
    # api.retrieve_paper("肝癌")
    # api.get_entity_similarity("心脏病", "糖尿病")
    print(api.get_word_cut("光觉检查,急诊科,小儿睾丸扭转,天麻素片,大蒜,万方制药,乌鸡汤,呼吸内科"))