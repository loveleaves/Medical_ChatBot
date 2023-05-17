# -*- coding:utf-8 -*-
import json
import pickle
import ahocorasick
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.preprocessing.sequence import pad_sequences

from knowledge_extraction.bilstm_crf.bilstm_crf_model import BiLstmCrfModel
from knowledge_extraction.bilstm_crf.config import config_params


class NerBaseDict(object):
    def __init__(self, dict_path):
        super(NerBaseDict, self).__init__()
        self.dict_path = dict_path
        self.region_words = self.load_dict(self.dict_path)
        self.region_tree = self.build_actree(self.region_words)

    def load_dict(self, path):
        with open(path, 'r', encoding='utf8') as f:
            return json.load(f)

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def recognize(self, text):
        item = {"string": text, "entities": []}

        region_wds = []
        for i in self.region_tree.iter(text):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        item["entities"] = [{"word": i, "type": "disease", "recog_label": "dict"} for i in final_wds]
        return item


class MedicalNerModel(object):
    """基于bilstm-crf的用于医疗领域的命名实体识别模型"""

    def __init__(self):
        super(MedicalNerModel, self).__init__()
        self.word2id, _, self.id2tag = pickle.load(
            open(config_params["word_tag_id"], "rb")
        )
        self.model, _ = BiLstmCrfModel(
            config_params['max_len'],
            config_params['vocab_size'],
            config_params['embedding_dim'],
            config_params['lstm_units'],
            config_params['class_nums']
        ).build()
        self.model.load_weights(config_params["model_save_path"])

        self.nbd = NerBaseDict(config_params["diseases_file"])

    def tag_parser(self, string, tags):
        item = {"string": string, "entities": [], "recog_label": "model"}
        entity_name = ""
        flag = []
        for char, tag in zip(string, tags):
            if tag[0] == "B":
                if entity_name != "":
                    x = dict((a, flag.count(a)) for a in flag)
                    y = [k for k, v in x.items() if max(x.values()) == v]
                    item["entities"].append({"word": entity_name, "type": y[0]})
                    flag.clear()
                    entity_name = ""
                entity_name += char
                flag.append(tag[2:])
            elif tag[0] == "I":
                entity_name += char
                flag.append(tag[2:])
            else:
                if entity_name != "":
                    x = dict((a, flag.count(a)) for a in flag)
                    y = [k for k, v in x.items() if max(x.values()) == v]
                    item["entities"].append({"word": entity_name, "type": y[0]})
                    flag.clear()
                flag.clear()
                entity_name = ""

        if entity_name != "":
            x = dict((a, flag.count(a)) for a in flag)
            y = [k for k, v in x.items() if max(x.values()) == v]
            item["entities"].append({"word": entity_name, "type": y[0]})

        return item

    def predict(self, texts: list):
        """
        texts 为一维列表，元素为字符串
        example : ["淋球菌性尿道炎的症状","上消化道出血的常见病与鉴别"]
        """
        # choose ner ans
        # strategy: dict > model
        if isinstance(texts, str):
            texts = [texts]

        res = []
        # nbd ner ans
        for text in texts:
            ents = self.nbd.recognize(text)
            if ents["entities"]:
                res.append(ents)
        if res:
            return res

        X = [[self.word2id.get(word, 1) for word in list(x)] for x in texts]
        X = pad_sequences(X, maxlen=config_params['max_len'], value=0)
        pred_id = self.model.predict(X)
        for text, pred in zip(texts, pred_id):
            tags = np.argmax(pred, axis=1)
            tags = [self.id2tag[i] for i in tags if i != 0]
            ents = self.tag_parser(text, tags)
            if ents["entities"]:
                res.append(ents)

        return res


global graph, model, sess

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

model = MedicalNerModel()


def NER_model(texts):
    if isinstance(texts, str):
        with graph.as_default():
            set_session(sess)
            result = model.predict(texts)
            return result

    elif isinstance(texts, list):
        results = []
        for text in texts:
            with graph.as_default():
                set_session(sess)
                result = model.predict(text)
                results.append(result)

        return results

    else:
        return "不支持该输入类型！"


if __name__ == '__main__':
    while True:
        text_list = input("pls input:")
        with graph.as_default():
            set_session(sess)
            result = model.predict(text_list)
        print(result)
