# coding=utf-8
BERT_DIR = "../../nlu/bert_intent_recognition/bert_weight_files/bert_wwm/"
MODEL_DIR = "./checkpoint/"
DATASET_DIR = "./data/"

bert_params = {
    "config": BERT_DIR + 'bert_config.json',
    "vocab": BERT_DIR + 'vocab.txt',
    "checkpoint": BERT_DIR + 'bert_model.ckpt',
}

config_params = {
    "train_file": DATASET_DIR + "train.txt",
    "dev_file": DATASET_DIR + "dev.txt",
    "test_file": DATASET_DIR + "test.txt",
    "diseases_file": MODEL_DIR + "diseases.json",
    "crf_trans": MODEL_DIR + "crf_trans.pkl",
    "model_save": MODEL_DIR + 'bert_bilstm_crf.weights'
}
