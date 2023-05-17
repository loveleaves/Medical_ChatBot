# coding=utf-8

MODEL_DIR = "./checkpoint/"
# DATASET_DIR = "./data/"
DATASET_DIR = "./DIY_data/"

# cMedQANER
# config_params = {
#     "epochs": 60,
#     "batch_size": 128,
#     "max_len": 250,
#     "vocab_size": 2410,
#     "embedding_dim": 200,
#     "lstm_units": 250,
#     "class_nums": 24,
#     "train_file": DATASET_DIR + "train.txt",
#     "dev_file": DATASET_DIR + "dev.txt",
#     "test_file": DATASET_DIR + "test.txt",
#     "word_tag_id": MODEL_DIR + "word_tag_id.pkl",
#     "diseases_file": MODEL_DIR + "diseases.json",
#     "model_save_path": MODEL_DIR + "best_bilstm_crf_model.h5",
# }

# diy_data
config_params = {
    "epochs": 30,
    "batch_size": 64,
    "max_len": 30,
    "vocab_size": 2410,
    "embedding_dim": 200,
    "lstm_units": 30,
    "class_nums": 4,
    "train_file": DATASET_DIR + "train.txt",
    "dev_file": DATASET_DIR + "dev.txt",
    "test_file": DATASET_DIR + "test.txt",
    "word_tag_id": MODEL_DIR + "word_tag_id.pkl",
    "diseases_file": MODEL_DIR + "diseases.json",
    "model_save_path": MODEL_DIR + "best_bilstm_crf_model.h5",
}
