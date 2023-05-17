#! -*- coding: utf-8 -*-
from sklearn.metrics import classification_report

from nlu.bert_intent_recognition.bert_model import build_bert_model
from nlu.bert_intent_recognition.data_helper import load_data
from nlu.bert_intent_recognition.config import config
from nlu.bert_intent_recognition.train import data_generator

def test():
    # 加载数据集
    test_data = load_data(config['test_data'])
    # 转换数据集
    test_generator = data_generator(test_data, config['batch_size'])

    model = build_bert_model(config['bert_config_path'], config['bert_checkpoint_path'], config['class_nums'])
    model.load_weights(config['model_save_path'])

    test_pred = []
    for x, y in test_generator:
        p = model.predict(x).argmax(axis=1)
        test_pred.extend(p)

    test_true = test_data[:, 1].tolist()
    # print(set(test_true))
    # print(set(test_pred))

    target_names = [line.strip() for line in open(config['label_path'], 'r', encoding='utf8')]
    print(classification_report(test_true, test_pred, target_names=target_names))

if __name__ == "__main__":
    test()