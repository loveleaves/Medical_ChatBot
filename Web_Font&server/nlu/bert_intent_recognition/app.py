# -*- coding:utf-8 -*-
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from bert4keras.tokenizers import Tokenizer

from nlu.bert_intent_recognition.bert_model import build_bert_model
from nlu.bert_intent_recognition.config import config as train_config


class BertIntentModel(object):
    def __init__(self):
        super(BertIntentModel, self).__init__()
        self.dict_path = train_config['bert_dict_path']
        self.config_path = train_config['bert_config_path']
        self.checkpoint_path = train_config['bert_checkpoint_path']

        self.label_list = [line.strip() for line in open(train_config['label_path'], 'r', encoding='utf8')]
        self.id2label = {idx: label for idx, label in enumerate(self.label_list)}

        self.tokenizer = Tokenizer(self.dict_path)
        self.model = build_bert_model(self.config_path, self.checkpoint_path, train_config['class_nums'])
        self.model.load_weights(train_config['model_save_path'])

    def predict(self, text):
        token_ids, segment_ids = self.tokenizer.encode(text, maxlen=60)
        proba = self.model.predict([[token_ids], [segment_ids]])
        rst = {l: p for l, p in zip(self.label_list, proba[0])}
        rst = sorted(rst.items(), key=lambda kv: kv[1], reverse=True)
        name, confidence = rst[0]
        return {"name": name, "confidence": float(confidence)}


global graph, sess

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

BIM = BertIntentModel()


def IR_model(texts):
    if isinstance(texts, str):
        with graph.as_default():
            set_session(sess)
            result = BIM.predict(texts)
            return result

    elif isinstance(texts, list):
        results = []
        for text in texts:
            with graph.as_default():
                set_session(sess)
                result = BIM.predict(text)
                results.append(result)
        return results

    else:
        return "不支持该类型输入！"


if __name__ == '__main__':
    while True:
        text = input("pls input: ")
        with graph.as_default():
            set_session(sess)
            result = BIM.predict(text)
        print(result)
