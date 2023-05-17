# coding=utf-8
import json
import os
from tqdm import tqdm
import random
import sys
# print(sys.path)
import pandas

from knowledge_extraction.bilstm_crf.train import Manage_Diseases
from utils.cpubmed_api_utils import CpubMedApi
from utils.visual_utils import VisualData


class BIO_Data:
    """
    function : 制作、导入BIO数据
    CMeEE数据集实体标签：{'bod', 'dep', 'dis', 'sym', 'mic', 'ite', 'dru', 'pro', 'equ'}
    即{疾病 (dis)，临床表现 (sym)，药物 (dru)，医疗设备 (equ)，医疗程序 (pro)，身体 (bod)，医学检验项目 (ite)，微生物类 (mic)，科室 (dep)}
    """

    def pos_2_bio(self, file_name: str, target_file: str, **kwargs):
        CMeEE_2_cMedQANER = {
            'bod': 'body',
            'dep': 'department',
            'dis': 'disease',
            'sym': 'symptom',
            # 'mic' : '',
            'ite': 'test',
            'dru': 'drug',
            'pro': 'treatment',
            # 'equ' : ''
        }

        text_data = []
        bio_data = []
        diseases = []
        with open(file_name, 'r') as f:
            data = json.load(f)
        for item in data:
            text = list(item['text'])
            bio = ['O' for _ in range(len(text))]
            flag = False
            for entity in item['entities']:
                if entity['type'] in CMeEE_2_cMedQANER:
                    flag = True
                    start_idx = entity['start_idx']
                    end_idx = entity['end_idx']
                    entity_type = CMeEE_2_cMedQANER[entity['type']]
                    bio[start_idx] = "B_" + entity_type
                    bio[start_idx + 1:end_idx + 1] = ["I_" + entity_type for _ in range(end_idx - start_idx)]

                    if entity_type == 'disease':
                        diseases.append(entity['entity'])

            # 如果实体能转换成功
            if flag:
                text_data.extend(text)
                bio_data.extend(bio)

        if 'save_disease' in kwargs and kwargs['save_disease']:
            """
            function : 保存disease列表，用于app.py推理使用
            """
            Manage_Diseases()
            Manage_Diseases.add_diseases_list(diseases)

        self.save_bio(text_data, bio_data, target_file)

    def merge_data(self, *args, **kwargs):
        """
        function : 合并多个BIO格式的实体数据集
        paras : args（来源文件名列表），kwargs（目标文件名，数据集划分比例）
        Note : 来源文件名列表注意先后顺序，因为会影响CRF层（详细请看data_helpers.py文件）
        """
        text_data = []
        bio_data = []
        for file_name in args:
            if isinstance(file_name, list):
                for t in file_name:
                    with open(t, 'r') as f:
                        for line in f.readlines():
                            if line.strip() != '':
                                line_data = line.split(' ')
                                text_data.append(line_data[0].strip())
                                bio_data.append(line_data[1].strip())
            else:
                with open(file_name, 'r') as f:
                    for line in f.readlines():
                        if line.strip() != '':
                            line_data = line.split(' ')
                            text_data.append(line_data[0].strip())
                            bio_data.append(line_data[1].strip())

        assert len(text_data) == len(bio_data), "文本和bio不等长，数据有问题！"

        # 不进行数据集划分
        if 'target_file' in kwargs:
            target_file = kwargs['target_file']
            assert not os.path.exists(target_file), "目标文件已存在！"
            self.save_bio(text_data, bio_data, target_file)

        # 合并时进行数据集划分
        if 'target_dir' in kwargs:
            target_dir = kwargs['target_dir']
            train_file = os.path.join(target_dir, 'train.txt')
            test_file = os.path.join(target_dir, 'test.txt')
            dev_file = os.path.join(target_dir, 'dev.txt')
            dataset_size = len(text_data)
            assert not os.path.exists(train_file), "目标文件已存在！"
            assert not os.path.exists(test_file), "目标文件已存在！"
            assert not os.path.exists(dev_file), "目标文件已存在！"

            if 'train_num' not in kwargs or 'test_num' not in kwargs or 'dev_num' not in kwargs:
                train_num, dev_num, test_num = 7, 2, 1
            else:
                train_num, dev_num, test_num = kwargs['train_num'], kwargs['test_num'], kwargs['dev_num']

            # 防止中途截断
            def find_pos(data, pos: int) -> int:
                sign_list = ['。', '？', '！']
                result_pos = pos
                while True:
                    if data[result_pos] in sign_list:
                        return result_pos + 1
                    result_pos += 1

                assert 'a' == 'b', "找不到合适位置"

            train_split_pos = find_pos(text_data, int(train_num / 10 * dataset_size))
            train_text_data, train_bio_data = text_data[:train_split_pos], bio_data[:train_split_pos]
            dev_split_pos = find_pos(text_data, int((train_num + dev_num) / 10 * dataset_size))
            dev_text_data, dev_bio_data = text_data[train_split_pos:dev_split_pos], \
                bio_data[train_split_pos:dev_split_pos]
            test_text_data, test_bio_data = text_data[dev_split_pos:], bio_data[dev_split_pos:]

            self.save_bio(train_text_data, train_bio_data, train_file)
            self.save_bio(test_text_data, test_bio_data, test_file)
            self.save_bio(dev_text_data, dev_bio_data, dev_file)

    def save_bio(self, text_data, bio_data, target_file):
        """
        function : 保存为BIO标注文件
        """
        assert not os.path.exists(target_file), "目标文件已存在！"

        with open(target_file, 'a', encoding='utf-8') as f:
            for i in range(len(text_data)):
                f.write(text_data[i] + " " + bio_data[i] + "\n")


class MakeData:
    """
    function : BIO数据标注
    cMedQANER数据集实体标签：{'physiology', 'test', 'disease', 'time', 'drug',
        'symptom', 'body', 'department', 'crowd', 'feature', 'treatment'}
    """

    def __init__(self, file_name: str, target_name: str):
        self.file_name = file_name
        self.target_name = target_name

    def data_loader(self):
        """
        des : symptom_data.json为多线程爬取、逐个写入dict
         只使用其中的disease['jieshao']，并用rasa-nlu-trainer标注工具 标注数据
        """
        data = []
        with open(self.file_name, 'r') as f:
            for line in f.readlines():
                try:
                    disease = json.loads(line)
                except Exception as e:
                    # print(e)
                    # print(line)
                    continue
                data.append(disease['jieshao'])

        self.listToJosn(data)

    def listToJosn(self, data):
        """
        function : 转成 rasa-nlu-trainer标注工具 需要的格式
        """
        result = []
        for text in data:
            # 构造每条数据的格式
            item = {
                'text': text,
                'intent': '',
                'entities': []
            }
            result.append(item)

        # 添加字典外层关键字
        dic = {"rasa_nlu_data":
                   {"common_examples": result}
               }

        with open(self.target_name, 'w', encoding="utf-8") as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)


class RawdataToBIO:
    """
    function: 利用已有成熟工具识别生语料中的实体
        前提：需要读取的csv文件中要有"content"列
    """

    def __init__(self, filepath, targetpath):
        self.file_path = filepath
        self.target_file = targetpath

    def get_start_index(self, sent: str, word: str) -> list:
        """
        function: 得到实体开始和结束索引
        """
        flag = True
        for i in range(len(sent)):
            if sent[i] == word[0]:
                for j in range(len(word)):
                    if sent[i + j] != word[j]:
                        flag = False
                        break
                if flag:
                    return [i, i + len(word)]
        assert False, "使用错误"

    def save_bio(self, text_data, bio_data, target_file):
        """
        function : 保存为BIO标注文件
        """
        assert not os.path.exists(target_file), "目标文件已存在！"
        with open(target_file, 'a', encoding='utf-8') as f:
            for i in range(len(text_data)):
                f.write(text_data[i] + " " + bio_data[i] + "\n")

    def raw_data_ner(self):
        """
        function: 利用已有成熟工具识别生语料中的实体
        前提：需要读取的csv文件中要有"content"列
        """
        assert os.path.exists(self.file_path), "文件不存在!"
        df = pandas.read_csv(self.file_path)
        try:
            raw_data = df['content']
        except:
            assert False, "csv文件没有content列"

        text_data = []
        bio_data = []
        ner = CpubMedApi()
        for line in raw_data:
            ans = ner.get_word_cut(line)
            for item in ans:
                if item[1] == "疾病":
                    text_data.append(line)
                    start_index, end_index = self.get_start_index(line, item[0])
                    bio = ["O" for i in range(len(line))]
                    bio[start_index] = "B_disease"
                    bio[start_index + 1:end_index] = ["I_disease" for _ in range(end_index - start_index - 1)]
                    bio_data.append(bio)

        self.save_bio(text_data, bio_data, self.target_file)


class CMID:
    """
    function: 处理CMID数据集
    """

    def __init__(self):
        self.file_path = "CMID/CMID.json"
        self.target_file = "CMID/CMID.txt"

    def extract_data(self):
        """
        function: 抽取所需数据类别
        needed_class: [疾病和诊断, 药物, 手术]
         前提： label4不是“其他”
        """
        assert os.path.exists(self.file_path), "CIMD数据集不存在！"
        with open(self.file_path, 'r') as f:
            raw_data = json.load(f)

        text_data = []
        bio_data = []
        needed_class = ['疾病和诊断', '药物', '手术']
        needed_class_dict = {
            '疾病和诊断': 'disease',
            '药物': 'drug',
            '手术': 'treatment'
        }
        for line in raw_data:
            if line['label_4class'] != "其他" and line['entities']:
                flag = False
                bio = ["O" for i in range(len(line['originalText']))]
                for entity in line['entities']:
                    if entity['label_type'] in needed_class:
                        start_index, end_index = int(entity['start_pos']), int(entity['end_pos'])
                        bio[start_index] = "B_" + needed_class_dict[entity['label_type']]
                        i_sign = "I_" + needed_class_dict[entity['label_type']]
                        bio[start_index + 1: end_index] = [i_sign for _ in range(end_index - start_index - 1)]
                        flag = True

                if flag:
                    bio_data.extend(bio)
                    text_data.extend(line['originalText'])

        self.save_bio(text_data, bio_data)

    def save_bio(self, text_data, bio_data):
        """
        function : 保存为BIO标注文件
        """
        assert not os.path.exists(self.target_file), "目标文件已存在！"

        with open(self.target_file, 'a', encoding='utf-8') as f:
            for i in range(len(text_data)):
                f.write(text_data[i] + " " + bio_data[i] + "\n")


class DIY_GenerateData:
    def __init__(self):
        self.data_path = "./DIY_data/data.json"
        self.bio_path = "./DIY_data/bio.txt"
        self.bio_train_path = "./DIY_data/train.txt"
        self.bio_val_path = "./DIY_data/dev.txt"
        self.bio_test_path = "./DIY_data/test.txt"

    def save_rawdata(self, data: list, shuffle=True):
        """
        function: save raw data
            data example: [{"originalText": "我不小心得了感冒要怎么治疗？",
                        "entities": [{"label_type": "disease", "start_pos": 6, "end_pos": 8}]},...]
        """
        assert not os.path.exists(self.data_path), "文件已存在!"

        if shuffle:
            random.shuffle(data)

        with open(self.data_path, 'a', encoding='utf-8') as f:
            for line in data:
                f.write(json.dumps(line, ensure_ascii=False))
                f.write("\n")

    def get_data_num(self, data_path="", split=False):
        """
        function: 获取数据集数据量
        """
        if not data_path:
            data_path = self.data_path
        assert os.path.exists(data_path), "文件不存在！"

        with open(data_path, 'r') as f:
            data_num = len(f.readlines())

        if split:
            train_num = int(data_num*0.7)
            dev_num = int(data_num*0.2)
            test_num = int(data_num*0.1)
            return train_num, dev_num, test_num
        else:
            return data_num

    def show_maxlen(self):
        """
        function: 显示句子长度分布
        """
        assert os.path.exists(self.data_path), "文件不存在,无法显示!"

        text_data = []
        with open(self.data_path, 'r') as f:
            for line in f.readlines():
                text_data.append(json.loads(line)['originalText'])

        visualer = VisualData()
        visualer.show_maxlen(text_data)

    def save_bio(self, text_data: list, bio_data: list, target_file=""):
        """
        function : 保存为BIO标注文件
        """
        if target_file:
            target_bio_path = target_file
        else:
            target_bio_path = self.bio_path
        assert not os.path.exists(target_bio_path), "目标文件已存在！"
        assert len(text_data) == len(bio_data), "数据长度不一致，有错误！"

        with open(target_bio_path, 'a', encoding='utf-8') as f:
            for i in range(len(text_data)):
                f.write(text_data[i] + " " + bio_data[i] + "\n")

    def make_bio(self, original_data: list, target_file: str):
        """
        function: 根据原始数据构建并bio数据
        """
        text_data = []
        bio_data = []

        for line in original_data:
            text = line['originalText']
            bio = ['O' for _ in range(len(text))]
            start_index = int(line['entities'][0]['start_pos'])
            end_index = int(line['entities'][0]['end_pos'])
            bio[start_index] = "B_disease"
            bio[start_index + 1:end_index] = ["I_disease" for _ in range(end_index - start_index - 1)]

            text_data.extend(text)
            bio_data.extend(bio)

        self.save_bio(text_data, bio_data, target_file=target_file)

    def generate(self, shuffle=True, data_split=True):
        """
        function: make NER data
        """
        assert not os.path.exists(self.data_path), "data文件已存在！"
        assert not os.path.exists(self.bio_path), "目标bio文件已存在！"
        original_data = []

        diseases = get_diseases()
        for item in tqdm(diseases, desc="正在创建数据集"):
            original_examples = self.generate_examples(item)
            original_data.extend(original_examples)

        if shuffle:
            random.shuffle(original_data)

        # save data
        self.save_rawdata(original_data)

        # save bio data
        if data_split:
            data_n = len(original_data)

            train_pos = int(0.7 * data_n)
            train_data = original_data[:train_pos]
            self.make_bio(train_data, target_file=self.bio_train_path)

            val_pos = int(0.2 * data_n)
            val_data = original_data[train_pos:train_pos + val_pos]
            self.make_bio(val_data, target_file=self.bio_val_path)

            test_data = original_data[train_pos + val_pos:]
            self.make_bio(test_data, target_file=self.bio_test_path)
        else:
            self.make_bio(original_data, target_file=self.bio_path)

    def generate_examples(self, disease):
        """
        function: 根据疾病构造数据集
        """
        original_examples = []

        # 可用开源数据集中的实体进行构建，如下面可用crowd代替
        subjects = ["", "我", "不小心", "人", "小孩", "大人", "老人"]
        get_expressions = ["得了", "患上", "感染"]
        sub_verb = []
        for sub in subjects:
            for verb in get_expressions:
                sub_verb.append(sub + verb)

        cure_examples = ["怎么治疗", "治疗方式", "怎么治"]
        for item in cure_examples:
            for sv in sub_verb:
                original_examples.append({"originalText": f"{sv}{disease}{item}？",
                                          "entities": [{"label_type": "disease", "start_pos": len(sv),
                                                        "end_pos": len(sv) + len(disease)}]})

        symptom_examples = ["症状", "表现"]
        for item in symptom_examples:
            for verb in get_expressions:
                original_examples.append({"originalText": f"{verb}{disease}有什么{item}？",
                                          "entities": [{"label_type": "disease", "start_pos": len(verb),
                                                        "end_pos": len(verb) + len(disease)}]})

        food_examples = ["可以吃什么", "推荐食物", "推荐菜谱", "推荐吃什么", "可以吃些什么", "忌吃食物", "不可以吃什么",
                         "建议吃什么", "不建议吃什么", "不推荐吃什么"]
        for item in food_examples:
            for sv in sub_verb:
                original_examples.append({"originalText": f"{sv}{disease}{item}？",
                                          "entities": [{"label_type": "disease", "start_pos": len(sv),
                                                        "end_pos": len(sv) + len(disease)}]})

        drug_examples = ["可以吃什么药", "推荐药品", "推荐吃什么药品", "可以吃些什么药", "需要吃些什么药"]
        for item in drug_examples:
            for sv in sub_verb:
                original_examples.append({"originalText": f"{sv}{disease}{item}？",
                                          "entities": [{"label_type": "disease", "start_pos": len(sv),
                                                        "end_pos": len(sv) + len(disease)}]})

        check_examples = ["要做什么检查", "需要做哪些检查"]
        for item in check_examples:
            for sv in sub_verb:
                original_examples.append({"originalText": f"{sv}{disease}{item}？",
                                          "entities": [{"label_type": "disease", "start_pos": len(sv),
                                                        "end_pos": len(sv) + len(disease)}]})

        des_examples = ["", "什么是", "什么叫"]
        for item in des_examples:
            original_examples.append({"originalText": f"{item}{disease}？",
                                      "entities": [{"label_type": "disease", "start_pos": len(item),
                                                    "end_pos": len(item) + len(disease)}]})

        dep_examples = ["", "要挂什么", "要看什么", "要挂哪个", "要去哪个"]
        for item in dep_examples:
            for sv in sub_verb:
                original_examples.append({"originalText": f"{sv}{disease}{item}科室？",
                                          "entities": [{"label_type": "disease", "start_pos": len(sv),
                                                        "end_pos": len(sv) + len(disease)}]})

        return original_examples


def get_diseases() -> list:
    """
    function: 读取爬取的疾病实体
    """
    with open("../../build_kg/graph_data/diseases.json", 'r') as f:
        diseases = json.load(f)

    return diseases


class VisualNERData(VisualData):
    def __init__(self):
        super().__init__()

    def cMedQANER_show_maxlen(self):
        """
        function: 可视化cMedQANER数据集数据的数据长度分布
        """
        dataset_dir = "./cMedQANER/"
        data_file = ["train.json", "dev.json", "test.json"]

        text_data = []
        for file in data_file:
            with open(dataset_dir+file, 'r') as f:
                for line in f.readlines():
                    text_data.append(json.loads(line)['text'])

        self.show_maxlen(text_data)

    def CMID_show_maxlen(self):
        """
        function: 可视化CMID数据集数据的数据长度分布
        """
        dataset_dir = "./CMID/"
        data_file = ["CMID.json"]

        text_data = []
        for file in data_file:
            with open(dataset_dir + file, 'r') as f:
                data = json.load(f)
                for line in data:
                    text_data.append(line['originalText'])

        self.show_maxlen(text_data)

if __name__ == "__main__":
    # file = "../../build_kg/symptom_data.json"
    # target = "./symptom_data.json"

    # 导出数据自己用标注工具标注数据
    # data_loader = MakeData(file, target)
    # data_loader.data_loader()

    # CMeEE数据集转成cMedQANER数据集的BIO格式
    # train_file_path = "./CMeEE/CMeEE_train.json"
    # target_train_file_path = "./CMeEE/CMeEE_train.txt"
    # dev_file_path = "./CMeEE/CMeEE_dev.json"
    # target_dev_file_path = "./CMeEE/CMeEE_dev.txt"
    # BIO = BIO_Data()
    # BIO.pos_2_bio(train_file_path, target_train_file_path)
    # BIO.pos_2_bio(dev_file_path, target_dev_file_path)
    # merge_file = ['./cMedQANER/train.txt', './cMedQANER/dev.txt',
    #               './CMID/CMID.txt', './cMedQANER/test.txt']
    # BIO.merge_data(merge_file, target_dir="./data")

    # NER = RawdataToBIO("cMedQA2/question.csv")
    # NER.raw_data_ner()

    # CMIDer = CMID()
    # CMIDer.extract_data()

    diy_data = DIY_GenerateData()
    # diy_data.generate()
    # diy_data.show_maxlen()
    print(diy_data.get_data_num(split=True))

    # visualer = VisualNERData()
    # visualer.cMedQANER_show_maxlen()