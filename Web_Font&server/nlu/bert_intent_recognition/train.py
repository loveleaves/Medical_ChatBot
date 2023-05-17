#! -*- coding: utf-8 -*-
import os
import numpy as np
from bert4keras.backend import keras
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding, DataGenerator
from sklearn.metrics import classification_report
from bert4keras.optimizers import Adam

from nlu.bert_intent_recognition.bert_model import build_bert_model
from nlu.bert_intent_recognition.data_helper import load_data
from nlu.bert_intent_recognition.config import config

tokenizer = Tokenizer(config['bert_dict_path'])


class data_generator(DataGenerator):
    """
    数据生成器
    """

    def __iter__(self, random=False):
        batch_token_ids, batch_segment_ids, batch_labels = [], [], []
        for is_end, (text, label) in self.sample(random):
            token_ids, segment_ids = tokenizer.encode(text, maxlen=config['maxlen'])  # [1,3,2,5,9,12,243,0,0,0]
            batch_token_ids.append(token_ids)
            batch_segment_ids.append(segment_ids)
            batch_labels.append([label])
            if len(batch_token_ids) == self.batch_size or is_end:
                batch_token_ids = sequence_padding(batch_token_ids)
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_labels = sequence_padding(batch_labels)
                yield [batch_token_ids, batch_segment_ids], batch_labels
                batch_token_ids, batch_segment_ids, batch_labels = [], [], []


def train():
    # 加载数据集
    train_data = load_data(config['train_data'])
    test_data = load_data(config['test_data'])
    train_data = np.r_[train_data, test_data]

    # 转换数据集
    train_generator = data_generator(train_data, config['batch_size'])
    test_generator = data_generator(test_data, config['batch_size'])

    model = build_bert_model(config['bert_config_path'], config['bert_checkpoint_path'], config['class_nums'])
    print(model.summary())

    best_model_filepath = config['model_save_path']
    if os.path.exists(best_model_filepath):
        model.load_weights(best_model_filepath)

    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=Adam(config['lr']),
        metrics=['accuracy'],
    )

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=3,
        verbose=2,
        mode='max'
    )
    checkpoint = keras.callbacks.ModelCheckpoint(
        best_model_filepath,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )

    model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator),
        epochs=config['epoch'],
        validation_data=test_generator.forfit(),
        validation_steps=len(test_generator),
        shuffle=True,
        callbacks=[earlystop, checkpoint]
    )

    model.load_weights(best_model_filepath)
    test_pred = []
    for x, y in test_generator:
        p = model.predict(x).argmax(axis=1)
        test_pred.extend(p)

    test_true = test_data[:, 1].tolist()
    # print(set(test_true))
    # print(set(test_pred))

    target_names = [line.strip() for line in open(config['label_path'], 'r', encoding='utf8')]
    print(classification_report(test_true, test_pred, target_names=target_names))


if __name__ == '__main__':
    train()
