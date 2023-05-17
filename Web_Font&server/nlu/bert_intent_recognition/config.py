#! -*- coding: utf-8 -*-

DATASET_DIR = './data/'
BERT_WEIGHT_DIR = './bert_weight_files/bert_wwm/'
# BERT_WEIGHT_DIR = './bert_weight_files/roberta/'
MODEL_SAVE_DIR = './checkpoint/'

# 定义超参数和配置文件
config = {
    'lr': 5e-6,
    'epoch': 10,
    'class_nums': 18,  # 13
    'maxlen': 60,
    'batch_size': 32,
    'bert_config_path': BERT_WEIGHT_DIR + 'bert_config.json',
    'bert_checkpoint_path': BERT_WEIGHT_DIR + 'bert_model.ckpt',
    'bert_dict_path': BERT_WEIGHT_DIR + 'vocab.txt',
    'train_data': DATASET_DIR + 'train.csv',
    'test_data': DATASET_DIR + 'test.csv',
    'label_path': DATASET_DIR + 'label',
    'model_save_path': MODEL_SAVE_DIR + "best_model_bert_wwm.weights",
    # 'model_save_path' : MODEL_SAVE_DIR + "best_model_roberta.weights"
}
