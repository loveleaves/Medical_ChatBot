# coding=utf-8
from knowledge_extraction.bilstm_crf.bilstm_crf_model import BiLstmCrfModel
from knowledge_extraction.bilstm_crf.data_helpers import NerDataProcessor
from knowledge_extraction.bilstm_crf.metrics import *
from knowledge_extraction.bilstm_crf.config import config_params


# embedding table = 2410 * 200 #[bs,80,200]
def build_model(model_filepath):
    ndp = NerDataProcessor(config_params['max_len'], config_params['vocab_size'])
    # 构造tag2id
    _, _ = ndp.read_data(
        config_params['train_file'],
        is_training_data=True
    )
    test_X, test_y = ndp.read_data(
        config_params['test_file'],
        is_training_data=False
    )
    test_X, test_y = ndp.encode(test_X, test_y)

    class_nums = ndp.class_nums
    id2tag = ndp.id2tag
    # _,_,id2tag = pickle.load(
    #         open(config['model_dir'] + "word_tag_id.pkl","wb")
    # )

    bilstm_crf = BiLstmCrfModel(
        config_params['max_len'],
        config_params['vocab_size'],
        config_params['embedding_dim'],
        config_params['lstm_units'],
        class_nums
    )
    model, _ = bilstm_crf.build()
    model.load_weights(model_filepath)
    y_true, y_pred = [], []

    pred = model.predict(test_X)
    for t_oh, p_oh in zip(test_y, pred):
        t_oh = np.argmax(t_oh, axis=1)
        t_oh = [id2tag[i].replace('_', '-') for i in t_oh if i != 0]
        p_oh = np.argmax(p_oh, axis=1)
        p_oh = [id2tag[i].replace('_', '-') for i in p_oh if i != 0]

        y_true.append(t_oh)
        y_pred.append(p_oh)
    return y_true, y_pred


def calc_metrics(y_true, y_pred):
    f1 = f1_score(y_true, y_pred, suffix=False)
    p = precision_score(y_true, y_pred, suffix=False)
    r = recall_score(y_true, y_pred, suffix=False)
    acc = accuracy_score(y_true, y_pred)
    print("f1_score: {:.4f}, "
          "precision_score: {:.4f},"
          " recall_score: {:.4f}, "
          "accuracy_score: {:.4f}"
          .format(f1, p, r, acc)
          )
    print(classification_report(y_true, y_pred, digits=4, suffix=False))


if __name__ == "__main__":
    model_filepath = config_params['model_save_path']
    y_true, y_pred = build_model(model_filepath)
    calc_metrics(y_true, y_pred)
