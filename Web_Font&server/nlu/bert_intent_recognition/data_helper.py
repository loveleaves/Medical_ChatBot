#! -*- coding: utf-8 -*-
import json
import random
import pandas as pd
from collections import defaultdict

from nlu.bert_intent_recognition.config import config
from utils.visual_utils import VisualData


def gen_training_data(raw_data_path):
    """
    function : 生成训练数据
    数据集CMID：4个大类，36个小类
    """
    label_list = [line.strip() for line in open(config['label_path'], 'r', encoding='utf8')]
    # print(label_list)
    label2id = {label: idx for idx, label in enumerate(label_list)}

    data = []
    with open(raw_data_path, 'r', encoding='utf8') as f:
        origin_data = f.read()
        origin_data = eval(origin_data)

    label_set = set()
    for item in origin_data:
        text = item["originalText"]
        label_36class = item["label_36class"][0].strip("'")
        if len(text) > 60 and label_36class not in ["所属科室", "传染性", "治愈率", "治疗时间"]:
            continue
        label_class = item["label_4class"][0].strip("'")
        if label_class == "其他":
            if random.random() > 0.8:
                data.append([text, label_class, label2id[label_class]])
            continue

        label_set.add(label_class)
        if label_36class in label_list:
            data.append([text, label_36class, label2id[label_36class]])
        label_set.add(label_36class)

    # print(label_set)

    return data


def gen_sample_base_template():
    explain_qwds = ['能否介绍一下', '想了解', '可以问一下', '能否告知', '如何理解', '怎样解释', '可以介绍', '解释一下',
                    '解释解释']
    howtodo_qwds = ['怎样才能', '怎么做可以', '咋样', '咋', '如何', '如何才可以', '如何做', '怎样', '采取什么措施',
                    '什么手段可以', '采取什么方法', \
                    '什么方法能', '怎么做', '我该如何', '我该咋样', '我该怎样', '']
    relevance_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现',
                      '伴随发生', '伴随', '共现', '其他病并发']
    greet_qwds = ['你好，麻烦问一下', '打扰问一下', '', '', '您好', '请问得了', '请教一下', '冒昧问一下', '问一下', '',
                  '如果得了', '']
    define_qwds = ['有什么定义？', '定义的意思', '的定义', '是什么意思？', '是啥意思', '是啥？', '的意思是什么', '的介绍',
                   '的释义', '解释', '介绍']
    department_qwds = ['属于什么科', '要看什么科', '可以挂什么科', '要挂什么科室', '看什么医生', '应该看啥医生',
                       '可以看啥科室', '挂啥科', '看啥科呢']
    infect_qwds = ['会传染给其他人吗？', '有传染性吗', '能感染到其他人吗', '是否会传染？', '传染性强吗', '会传给孩子吗',
                   '会传给老人吗', '会传给孕妇吗', \
                   '会人传人不？', '易感人群是什么人', '容易感染不', '易发人群是哪些人', '我会感染吗', '我会染上吗',
                   '会让我得上吗', '会传染给哪些人', '什么人容易得']
    cureprob_qwds = ['多大概率能治好？', '多大几率能治好', '治好希望大么？', '痊愈几率', '治愈概率几成', '治愈比例',
                     '治好的可能性', '能治吗', '可治率多高？', \
                     '可以治好吗', '能否治好', '治愈率多高', '能治好不']
    check_qwds = ['需要做什么检查', '要检查啥项目？', '如何体检', '检查什么', '做啥体检呢？', '如何体检？',
                  '要做什么化验治疗吗', '化验什么啊', '做啥检查']
    prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉',
                    '躲开', '躲掉', '绕开']
    lasttime_qwds = ['的治疗周期', '要治多久', '治疗多长时间', '治疗多少时间', '治疗几天', '治愈需要几年',
                     '治好要多少天', '要治几多时间', '得治疗几个小时', \
                     '治好得多少年', '要花多少时间治好', '完全治愈要多久', '治好要多久', '治疗时间长吗', '治疗周期？']
    symptom_qwds = ['症状', '的症状', '的症状是什么', '表征是啥', '现象', '症候', '临床表现', '病症表现', '病症是啥',
                    '病症是啥']
    getprob_qwds = ['多大概率得病？', '多大几率患病', '得病可能大么？', '患病几率', '患病概率几成', '患病比例',
                    '患病的可能性', '可能吗', '得病可能性多高？', \
                    '可能得吗', '会有吗', '患病率多高', '会患上吗']
    # cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
    rec_qwds = ["", "推荐", "好评", "建议", "热销", "热卖", "合适", "最合适", "最好"]
    rec_food_qwds = ['饮食', '饮用', '吃什么', '食', '伙食', '膳食', '喝什么', '补品', '保健品', "吃的",
                     '食用', '食物', '补品']
    rec_recipe_qwds = ['菜', '食谱', '菜谱', "菜品", "菜单", "特色菜", "招牌菜"]
    drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
    # 
    # cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
    # cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
    # '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

    label_list = [line.strip() for line in open(config['label_path'], 'r', encoding='utf8')]
    label2id = {label: idx for idx, label in enumerate(label_list)}

    disease_list = json.load(
        open('../../build_kg/graph_data/diseases.json', 'r', encoding='utf8'))
    n = len(disease_list) - 1

    data = []

    # 询问疾病定义模板，example : 请问什么是XX疾病?
    template = "{greet}{explain}{disease}{define}"
    for i in range(60):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        explain = explain_qwds[random.randint(0, len(explain_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        define = define_qwds[random.randint(0, len(define_qwds) - 1)]
        text = template.format(greet=greet, explain=explain, disease=disease, define=define)
        data.append([text, '定义', label2id['定义']])

    # 询问临床表现(病症表现)模板，example : 请问得了XX疾病有什么症状?
    template = "{greet}{disease}{symptom}"
    for i in range(60):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        symptom = symptom_qwds[random.randint(0, len(symptom_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, symptom=symptom)
        data.append([text, '临床表现(病症表现)', label2id['临床表现(病症表现)']])

    # 询问预防措施模板，example : 请问XX疾病怎么预防?
    template = "{howtodo}{prevent}{disease}"
    for i in range(100):
        howtodo = howtodo_qwds[random.randint(0, len(howtodo_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        prevent = prevent_qwds[random.randint(0, len(prevent_qwds) - 1)]
        text = template.format(howtodo=howtodo, disease=disease, prevent=prevent)
        data.append([text, '预防', label2id['预防']])

    # 询问相关病症模板，example : 请问XX疾病有什么相关病吗?
    template = "{greet}{disease}有什么{relevance}"
    for i in range(80):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        relevance = relevance_qwds[random.randint(0, len(relevance_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, relevance=relevance)
        data.append([text, '相关病症', label2id['相关病症']])

    # 询问所属科室模板，example : 请问XX疾病应该看什么科?
    template = "{greet}{disease}{department}"
    for i in range(100):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        department = department_qwds[random.randint(0, len(department_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, department=department)
        data.append([text, '所属科室', label2id['所属科室']])

    # 询问传染性模板，example : 请问XX疾病会传染哪些人群？
    template = "{greet}{disease}{infect}"
    for i in range(120):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        infect = infect_qwds[random.randint(0, len(infect_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, infect=infect)
        data.append([text, '传染性', label2id['传染性']])

    # 询问治愈率模板，example : 请问得了XX疾病的治愈率多高？
    template = "{greet}{disease}{cureprob}"
    for i in range(120):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        cureprob = cureprob_qwds[random.randint(0, len(cureprob_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, cureprob=cureprob)
        data.append([text, '治愈率', label2id['治愈率']])

    # 询问化验/体检方案模板，example : 请问得了XX疾病要做什么检查？
    template = "{greet}{disease}{check}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        check = check_qwds[random.randint(0, len(check_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, check=check)
        data.append([text, '化验/体检方案', label2id['化验/体检方案']])

    # 询问治疗时间模板，example : 请问得了XX疾病要治疗多久？
    template = "{greet}{disease}{lasttime}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        lasttime = lasttime_qwds[random.randint(0, len(lasttime_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, lasttime=lasttime)
        data.append([text, '治疗时间', label2id['治疗时间']])

    # 询问患病概率模板，example : 请问XX疾病患病概率有多高？
    template = "{greet}{disease}{getprob}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        getprob = getprob_qwds[random.randint(0, len(getprob_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, getprob=getprob)
        data.append([text, '患病概率', label2id['患病概率']])

    # 询问推荐食物模板，example : 请问XX疾病推荐吃什么食物？
    template = "{greet}{disease}{rec_word}{rec_food}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        rec_food = rec_food_qwds[random.randint(0, len(rec_food_qwds) - 1)]
        rec_word = rec_qwds[random.randint(0, len(rec_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, rec_word=rec_word, rec_food=rec_food)
        data.append([text, '推荐食物', label2id['推荐食物']])

    # 询问推荐菜谱模板，example : 请问XX疾病推荐吃什么菜？
    template = "{greet}{disease}{rec_word}{rec_recipe}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        rec_recipe = rec_recipe_qwds[random.randint(0, len(rec_recipe_qwds) - 1)]
        rec_word = rec_qwds[random.randint(0, len(rec_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, rec_word=rec_word, rec_recipe=rec_recipe)
        data.append([text, '推荐菜谱', label2id['推荐菜谱']])

    # 询问通用药品模板，example : 请问XX疾病一般吃什么药？
    common_qwds = ["一般", "通用", "常用", "普遍", "常见"]
    template = "{greet}{disease}{common_word}{drug_word}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        drug_word = drug_qwds[random.randint(0, len(drug_qwds) - 1)]
        common_word = common_qwds[random.randint(0, len(common_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, common_word=common_word, drug_word=drug_word)
        data.append([text, '通用药品', label2id['通用药品']])

    # 询问推荐药品模板，example : 请问XX疾病推荐吃什么药？
    template = "{greet}{disease}{rec_word}{drug_word}"
    for i in range(150):
        greet = greet_qwds[random.randint(0, len(greet_qwds) - 1)]
        disease = disease_list[random.randint(0, n)]
        if i % 15 == 0:
            disease == ""
        drug_word = drug_qwds[random.randint(0, len(drug_qwds) - 1)]
        rec_word = rec_qwds[random.randint(0, len(rec_qwds) - 1)]
        text = template.format(greet=greet, disease=disease, rec_word=rec_word, drug_word=drug_word)
        data.append([text, '推荐药品', label2id['推荐药品']])

    return data


def load_data(filename):
    """
    function : 加载数据
    return : 单条格式：(文本, 标签id)
    """
    df = pd.read_csv(filename, header=0)
    # print(df.shape)
    return df[['text', 'label']].values


class VisualIRData(VisualData):
    def __init__(self):
        super().__init__()

    def IRData_show_maxlen(self):
        """
        function: 可视化意图识别数据集数据的数据长度分布
        """
        dataset_dir = "./data/"
        data_file = ["train.csv", "test.csv"]
        # label_file = dataset_dir + "label"

        # label_list = [line.strip() for line in open(label_file, 'r', encoding='utf8')]

        text_data = []
        for file in data_file:
            df = pd.read_csv(dataset_dir + file, dtype={"text": str, "label_class": str, "label": int})
            for i in range(len(df)):
                text_data.append(df.iloc[i][0])

        self.show_maxlen(text_data)

    def print_class_num(self):
        """
        function: 统计所有类别数据量
        """
        dataset_dir = "./data/"
        data_file = ["train.csv", "test.csv"]

        data_num = defaultdict(int)
        for file in data_file:
            df = pd.read_csv(dataset_dir + file, dtype={"text": str, "label_class": str, "label": int})
            for i in range(len(df)):
                data_num[df.iloc[i][1]] += 1

        print(data_num)
        print(sum(data_num.values()))


def generate_data_main():
    """
    function: 构建训练数据
      利用数据集： Chinese Medical Intent Dataset(CMID)
    """
    data_path = "./raw_data/CMID.json"
    train_rate = 0.9
    data1 = gen_training_data(data_path)
    # df = pd.DataFrame(data1, columns=['text', 'label_class', 'label'])
    # print(df['label'].value_counts())
    data2 = gen_sample_base_template()

    data = data1 + data2
    data = pd.DataFrame(data, columns=['text', 'label_class', 'label'])
    data = data.sample(frac=1.0)
    # print(data['label_class'].value_counts())

    train_num = int(train_rate * len(data))
    train, test = data[:train_num], data[train_num:]
    train.to_csv("./data/train.csv", index=False)
    test.to_csv("./data/test.csv", index=False)


if __name__ == '__main__':
    # generate_data_main()
    visualer = VisualIRData()
    # visualer.IRData_show_maxlen()
    visualer.print_class_num()
