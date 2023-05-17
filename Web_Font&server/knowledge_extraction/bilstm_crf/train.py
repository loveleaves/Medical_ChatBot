# coding=utf-8
import keras
import pickle
import json
import os

from knowledge_extraction.bilstm_crf.bilstm_crf_model import BiLstmCrfModel
from knowledge_extraction.bilstm_crf.data_helpers import NerDataProcessor
from knowledge_extraction.bilstm_crf.metrics import *
from knowledge_extraction.bilstm_crf.config import config_params


def train():
    ndp = NerDataProcessor(config_params['max_len'], config_params['vocab_size'])
    train_X, train_y = ndp.read_data(
        config_params['train_file'],
        is_training_data=True
    )
    print("**********************Train data(before encode)*************************")
    print(train_X[:5], '\n')
    print(train_y[:5], '\n')
    train_X, train_y = ndp.encode(train_X, train_y)
    print("**********************Train data(after encode)*************************")
    print(train_X[:5], '\n')
    print(train_y[:5], '\n')

    dev_X, dev_y = ndp.read_data(
        config_params['dev_file'],
        is_training_data=False
    )
    dev_X, dev_y = ndp.encode(dev_X, dev_y)
    test_X, test_y = ndp.read_data(
        config_params['test_file'],
        is_training_data=False
    )
    test_X, test_y = ndp.encode(test_X, test_y)

    class_nums = ndp.class_nums
    print("class_nums: ", class_nums)
    word2id = ndp.word2id
    tag2id = ndp.tag2id
    id2tag = ndp.id2tag
    pickle.dump(
        (word2id, tag2id, id2tag),
        open(config_params["word_tag_id"], "wb")
    )

    bilstm_crf = BiLstmCrfModel(
        config_params['max_len'],
        config_params['vocab_size'],
        config_params['embedding_dim'],
        config_params['lstm_units'],
        class_nums
    )
    model, crf = bilstm_crf.build()

    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=4,
        verbose=1
    )

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        verbose=2,
        mode='min'
    )
    best_model_filepath = config_params["model_save_path"]
    if os.path.exists(best_model_filepath):
        model.load_weights(best_model_filepath)

    checkpoint = keras.callbacks.ModelCheckpoint(
        best_model_filepath,
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )
    model.fit(
        x=train_X,
        y=train_y,
        batch_size=config_params['batch_size'],
        epochs=config_params['epochs'],
        validation_data=(dev_X, dev_y),
        shuffle=True,
        callbacks=[reduce_lr, earlystop, checkpoint]
    )
    print(crf.chain_kernel)
    model.load_weights(best_model_filepath)

    pred = model.predict(test_X)

    y_true, y_pred = [], []

    for t_oh, p_oh in zip(test_y, pred):
        t_oh = np.argmax(t_oh, axis=1)
        t_oh = [id2tag[i].replace('_', '-') for i in t_oh if i != 0]
        p_oh = np.argmax(p_oh, axis=1)
        p_oh = [id2tag[i].replace('_', '-') for i in p_oh if i != 0]

        y_true.append(t_oh)
        y_pred.append(p_oh)

    f1 = f1_score(y_true, y_pred, suffix=False)
    p = precision_score(y_true, y_pred, suffix=False)
    r = recall_score(y_true, y_pred, suffix=False)
    acc = accuracy_score(y_true, y_pred)
    print(
        "f1_score: {:.4f}, precision_score: {:.4f}, recall_score: {:.4f}, accuracy_score: {:.4f}".format(f1, p, r, acc))
    print(classification_report(y_true, y_pred, digits=4, suffix=False))


class Manage_Diseases():
    def __int__(self):
        self.file_path = config_params["diseases_file"]

    def add_diseases_list(self, need_diseases: list):
        with open(self.file_path, 'r') as f:
            diseases = json.load(f)
        # print(type(diseases),len(diseases))
        diseases_dict = {disease: 1 for disease in diseases}
        need_add_diseases = []
        for disease in need_diseases:
            if disease not in diseases_dict:
                need_add_diseases.append(disease)
        diseases.extend(need_add_diseases)
        # print(diseases)
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=4)

    def add_diseases_file(self, file_path: str):
        with open(file_path, 'r') as f:
            need_diseases = json.load(f)
        with open(self.file_path, 'r') as f:
            diseases = json.load(f)
        # print(type(diseases),len(diseases))

        diseases_dict = {disease: 1 for disease in diseases}
        need_add_diseases = []
        for disease in need_diseases:
            if disease not in diseases_dict:
                need_add_diseases.append(disease)
        diseases.extend(need_add_diseases)
        # print(diseases)
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    train()
    # Manage_Diseases()
    # Manage_Diseases.add_diseases_list(["heat disease", "headache"])
