# -*- coding:utf-8 -*-

DATASET_DIR = "entity_normalization/data/"
RAW_DATASET_DIR = "entity_normalization/total/"
MODEL_DIR = "entity_normalization/checkpoint/"

data_params = {
    'train_file': DATASET_DIR + "train.csv",
    'train_extend_file': DATASET_DIR + "train_extend.csv",
    'test_file': DATASET_DIR + "test.csv",
    'code_file': RAW_DATASET_DIR + "code.txt"
}

raw_data_params = {
    'train_file': RAW_DATASET_DIR + "train.xlsx",
    'val_file': RAW_DATASET_DIR + "val.xlsx",
    'answer_file': RAW_DATASET_DIR + "answer.xlsx",
    'code_file': RAW_DATASET_DIR + "code.txt"
}

esim_params = {
    'num_classes': 2,
    'max_features': 1900,  # 3000
    'embed_size': 200,
    'embedding_matrix': [],
    'w_initializer': 'random_uniform',
    'b_initializer': 'zeros',
    'dropout_rate': 0.2,
    'mlp_activation_func': 'relu',
    'mlp_num_layers': 1,
    'mlp_num_units': 128,
    'mlp_num_fan_out': 128,
    'lstm_units': 30,
    'input_shapes': [(20,), (20,)],
    'task': 'Classification',
    'model_save_path': MODEL_DIR + 'best_esim_model.h5',
    'model_frame_path': MODEL_DIR + 'esim_model.json',
    'word2id': MODEL_DIR + 'word2id.pkl',
}
