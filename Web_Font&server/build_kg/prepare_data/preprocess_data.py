import json
import os
import re


class PreprocessData:
    """
    function: 预处理数据，每行json数据格式如下：
    {
        "url": "http:/..",
        "basic_info": {
                "category": ["疾病百科", "急诊科"],
                "name": "二硫化碳中毒", "desc": ["..."],
                "attributes": [
                        "医保疾病： 否 ", "患病比例：发病率约。。%",
                        "易感人群：。", "传染方式：无传染性",
                        "并发症：昏迷", "就诊科室：急诊科  ",
                        "治疗方式：药物治疗 支持性治疗", "治疗周期：1-2个月",
                        "治愈率：80-85% ", " 常用药品：  仁青芒觉 季德胜蛇药片",
                        "治疗费用：。。", "多食新鲜的水果和蔬菜，以保证维生素的摄入量。"
                    ]
            },
        "cause_info": "发病原因：\n。。",
        "prevent_info": "。以确保作业者的健康。。",
        "symptom_info": [
                ["徐清芝", "姜树锋", "刘琦", "王竹磊", "王竹磊"],
                ["急性中毒呈麻醉样作用。。。"]
            ],
        "inspect_info": [],
        "treat_info": [
                "就诊科室：急诊科  ", "治疗方式：药物治疗 支持性治疗",
                "治疗周期：1-2个月", "治愈率：80-85%", "常用药品： 。。",
                "治疗费用：根据不同病情，。。"
            ],
        "food_info": {
                "good": ["生菜", 。。], "bad": ["啤酒", 。。],
                "recommand": ["小麦粥",。。]
            },
        "drug_info": ["金诃藏药仁青芒觉(仁青芒觉)",。。]
    }
    """

    def __init__(self):
        self.raw_file = "raw_data.json"
        self.target_file = "data.json"

    def strip_str(self, s: str) -> str:
        """
        function: 去除str中\r\t\n\s等字符
        """
        ans = re.sub("\r|\t|\n|\s", "", s)
        return ans

    def strip_list(self, data: list) -> list:
        """
        function: 去除list中\r\t\n\s等字符
        """
        ans = []
        for item in data:
            item = str(item).strip()
            item = self.strip_str(item)
            ans.append(item)
        return ans

    def extract_prob(self, sent: str) -> str:
        """
        function: 从字符串中抽取数字
        """
        ans = [float(s) for s in re.findall(r'-?\d+\.?\d*', sent)]
        ans = [str(s) + "%" for s in ans]

        return "-".join(ans)

    def get_symptom(self, symptom: list) -> list:
        """
        function: 抽取症状
        """
        ans = []
        if not symptom:
            return ans

        # 跳过名字
        for item in symptom[1:]:
            ans.append(self.strip_list(item))
        return ans

    def extract_list_from_str(self, s: str) -> list:
        """
        function: 通过空格抽取字符串中多个实体
        """
        s = s.strip()
        ans = [self.strip_str(word) for word in s.split(' ')]

        return ans

    def extract_drug(self, drug_info: list) -> list:
        drug = []
        if not drug_info:
            return drug

        for item in drug_info:
            drug.append(self.strip_str(item.split('(')[1].strip(')')))

        return drug

    def extract_attributes(self, attributes: list, treat_info: list) -> dict:
        """
        function: 抽取疾病的属性
        """
        ans = {
            "yibao_status": "",
            "get_prob": "",
            "easy_get": "",
            "get_way": "",
            "acompany": [],
            "cure_department": [],
            "cure_way": [],
            "cure_lasttime": "",
            "cured_prob": "",
            "common_drug": [],
            "cost_money": "",
            "suggestion": "",
        }
        if not attributes:
            return ans

        ans['yibao_status'] = self.strip_str(attributes[0].split('：')[1])
        ans['get_prob'] = self.extract_prob(attributes[1])
        ans['easy_get'] = self.strip_str(attributes[2].split('：')[1])
        ans['get_way'] = self.strip_str(attributes[3].split('：')[1])
        ans['acompany'].extend(self.extract_list_from_str(attributes[4].split('：')[1]))

        ans['cure_department'].extend(self.extract_list_from_str(attributes[5].split('：')[1]))
        ans['cure_way'].extend(self.extract_list_from_str(attributes[6].split('：')[1]))
        ans['cure_lasttime'] = self.strip_str(attributes[7].split('：')[1])
        ans['cured_prob'] = self.extract_prob(attributes[8])
        ans['common_drug'].extend(self.extract_list_from_str(attributes[9].split('：')[1]))
        ans['cost_money'] = self.strip_str(attributes[10].split('：')[1])
        ans['suggestion'] = self.strip_str(attributes[11])

        if treat_info:
            # 当attributes中有些为空但treat_info不为空时，用treat_info填充
            if not ans['cure_department'] and len(treat_info[0].split('：')) > 1:
                ans['cure_department'].extend(self.extract_list_from_str(treat_info[0].split('：')[1]))
            if not ans['cure_way'] and len(treat_info[1].split('：')) > 1:
                ans['cure_way'].extend(self.extract_list_from_str(treat_info[1].split('：')[1]))
            if not ans['cure_lasttime'] and len(treat_info[2].split('：')) > 1:
                ans['cure_lasttime'] = self.extract_list_from_str(treat_info[2].split('：')[1])
            if not ans['cured_prob'] and len(treat_info[3].split('：')) > 1:
                ans['cured_prob'] = self.extract_list_from_str(treat_info[3].split('：')[1])
            if not ans['cost_money'] and len(treat_info[4].split('：')) > 1:
                ans['cost_money'] = self.extract_list_from_str(treat_info[4].split('：')[1])

        return ans

    def process_data(self):
        assert not os.path.exists(self.target_file), "目标文件已存在"
        target_f = open(self.target_file, 'a', encoding='utf-8')

        with open(self.raw_file, 'r') as f:
            for line in f.readlines():
                data = {"_id": "", "name": "", "desc": "", "category": [], "prevent": "",
                        "cause": "", "symptom": [], "yibao_status": "", "get_prob": "", "easy_get": "",
                        "get_way": "", "acompany": [], "cure_department": [], "cure_way": [], "cure_lasttime": "",
                        "cured_prob": "", "common_drug": [], "cost_money": "", "check": [], "do_eat": [],
                        "not_eat": [], "recommand_eat": [], "recommand_drug": [], "drug_detail": []
                        }
                line_data = json.loads(line)

                data['_id'] = self.strip_str(line_data['url'])
                data['name'] = self.strip_str(line_data['basic_info']['name'])
                if not data['name']:
                    continue
                data['desc'] = "".join(self.strip_list(line_data['basic_info']['desc']))
                data['category'].extend(self.strip_list(line_data['basic_info']['category']))
                data['prevent'] = self.strip_str(line_data['prevent_info'])
                data['cause'] = self.strip_str(line_data['cause_info'])
                data['symptom'].extend(self.get_symptom(line_data['symptom_info']))

                attributes = self.extract_attributes(line_data['basic_info']['attributes'],
                                                     line_data['treat_info'])
                data['yibao_status'] = attributes['yibao_status']
                data['get_prob'] = attributes['get_prob']
                data['easy_get'] = attributes['easy_get']
                data['get_way'] = attributes['get_way']
                data['acompany'].extend(attributes['acompany'])
                data['cure_department'].extend(attributes['cure_department'])
                data['cure_way'].extend(attributes['cure_way'])
                data['cure_lasttime'] = attributes['cure_lasttime']
                data['cured_prob'] = attributes['cured_prob']
                data['common_drug'].extend(attributes['common_drug'])
                data['cost_money'] = attributes['cost_money']

                data['check'].extend(self.strip_list(line_data['inspect_info']))
                data['do_eat'].extend(self.strip_list(line_data['food_info']['good']))
                data['not_eat'].extend(self.strip_list(line_data['food_info']['bad']))
                data['recommand_eat'].extend(self.strip_list(line_data['food_info']['recommand']))
                data['recommand_drug'].extend(self.extract_drug(line_data['drug_info']))
                data['drug_detail'].extend(self.strip_list(line_data['drug_info']))

                target_f.write(json.dumps(data, ensure_ascii=False))
                target_f.write("\n")

        target_f.close()


def count_json_line(file_path):
    with open(file_path, 'r') as f:
        print(len(f.readlines()))


if __name__ == "__main__":
    Data = PreprocessData()
    Data.process_data()
