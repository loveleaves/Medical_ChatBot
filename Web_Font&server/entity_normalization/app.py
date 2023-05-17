# -*- coding:utf-8 -*-
import json
import pickle
import random

import tensorflow as tf

from entity_normalization.esim import ESIM
from entity_normalization.data_helper import pad_sequences
from entity_normalization.bm25_retrival import BM25Retrieval
from keras.backend.tensorflow_backend import set_session
from entity_normalization.config import data_params, esim_params, MODEL_DIR


class EntityMatch(object):
    def __init__(self, kb_path):
        super(EntityMatch, self).__init__()
        self.kb_path = kb_path
        self.bm25re = BM25Retrieval(self.kb_path)

        self.word2idx, _ = pickle.load(open(esim_params['word2id'], "rb"))
        self.model = ESIM(esim_params).build()
        self.model.load_weights(esim_params['model_save_path'])

    def char_index(self, p_sentences, h_sentences):
        p_list, h_list = [], []
        for p_sentence, h_sentence in zip(p_sentences, h_sentences):
            p = [self.word2idx[word.lower()] for word in p_sentence if
                 len(word.strip()) > 0 and word.lower() in self.word2idx.keys()]
            h = [self.word2idx[word.lower()] for word in h_sentence if
                 len(word.strip()) > 0 and word.lower() in self.word2idx.keys()]

            p_list.append(p)
            h_list.append(h)

        p_list = pad_sequences(p_list, maxlen=esim_params['input_shapes'][0][0])
        h_list = pad_sequences(h_list, maxlen=esim_params['input_shapes'][0][0])

        return p_list, h_list

    def predict(self, query):
        cand_docs = self.bm25re.retrieval(query, 20)
        querys = [query] * len(cand_docs)

        p, h = self.char_index(querys, cand_docs)

        scores = self.model.predict([p, h])
        scores = scores[:, 1]
        match_score = {e: s for e, s in zip(cand_docs, scores)}
        match_score = sorted(match_score.items(), key=lambda x: x[1], reverse=True)
        return match_score[0], cand_docs


class Entity_Normalization(object):
    def __init__(self):
        super(Entity_Normalization, self).__init__()
        self.model = EntityMatch(data_params['code_file'])

    def predict(self, texts, threshold=0.8):
        if isinstance(texts, str):
            pred, cand_docs = self.model.predict(texts)
            if pred[1] > threshold:
                return pred[0]
            else:
                return texts

        elif isinstance(texts, list):
            results = []
            for text in texts:
                pred, cand_docs = self.model.predict(text)
                if pred[1] > threshold:
                    results.append(pred[0])
                else:
                    results.append(text)
            return results

        else:
            return "不支持该输入类型！"


def BD_search(word):
    file_path = MODEL_DIR + "alias_dict.json"
    with open(file_path, 'r') as f:
        data = json.load(f)

    if word in data.keys():
        return random.choice(data[word])
    else:
        return None


global graph, sess

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

EMM = Entity_Normalization()


def EMM_model(word, e_type="disease"):
    """
    function: 实体规范化
    增加BD_search优化规范化效果
    e_type: 规范化的实体类型，TODO
    """
    bd_ans = BD_search(word)
    if bd_ans:
        return bd_ans

    with graph.as_default():
        set_session(sess)
        result = EMM.predict(word)
        return result


if __name__ == '__main__':
    while True:
        text = input("请输入：")
        with graph.as_default():
            set_session(sess)
            result = EMM.predict(text)
            print(result)
