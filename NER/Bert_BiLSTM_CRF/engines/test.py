# -*- coding: utf-8 -*-
import copy
import math
import time
import os
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from pathlib import Path
from tensorflow_addons.text.crf import crf_decode

from Bert_BiLSTM_CRF_Model import Bert_BiLSTM_CRF_MODEL
from utils.metrics import metrics

model_name = 'bert-base-chinese'
MODEL_PATH = 'bert-base-chinese'

base_path = Path(__file__).resolve().parent.parent


def test(configs, data_manager, logger):
    vocab_size = data_manager.max_token_num
    num_classes = data_manager.max_label_num
    batch_size = configs.batch_size

    if configs.use_bert:
        tokenizer = data_manager.tokenizer
        X_test, y_test, att_mask_test = data_manager.get_test_set
    else:
        X_test, y_test, att_mask_test = data_manager.get_test_set
        bert_model, tokenizer = None, None

    bilstm_crf_model = tf.saved_model.load(os.path.join(base_path, configs.model_save_dir))
    # bilstm_crf_model = Bert_BiLSTM_CRF_MODEL(MODEL_PATH, configs, num_classes)
    # checkpoint = tf.train.Checkpoint(model=bilstm_crf_model)
    # checkpoint.restore(tf.train.latest_checkpoint(configs.checkpoints_dir))
    logger.info('loading model successfully...')

    num_test_iterations = int(math.ceil(len(X_test) / batch_size))
    start_time = time.time()
    test_results = {}
    test_labels_results = {}
    for label in data_manager.suffix:
        test_labels_results.setdefault(label, {})
    for measure in configs.measuring_metrics:
        test_results[measure] = 0
    for label in test_labels_results.keys():
        for measure in configs.measuring_metrics:
            test_labels_results[label][measure] = 0

    logger.info('+' * 30 + 'testing starting' + '+' * 30)
    for iteration in tqdm(range(num_test_iterations)):
        if configs.use_bert:
            X_test_batch, y_test_batch, _ = data_manager.next_batch(X_test,
                                                                    y_test,
                                                                    att_mask_test,
                                                                    iteration * batch_size)
            input_length_test = tf.math.count_nonzero(X_test_batch, 1)
            # model_inputs = copy.deepcopy(X_test_batch)
        else:
            X_test_batch, y_test_batch = data_manager.next_batch(X_test, y_test, iteration * batch_size)
            input_length_test = tf.math.count_nonzero(X_test_batch, 1)
            # model_inputs = copy.deepcopy(X_test_batch)

        logits_test, _, transition_params_test = bilstm_crf_model.call(inputs=[X_test_batch,
                                                                               input_length_test,
                                                                               y_test_batch])
        batch_pred_sequence_test, _ = crf_decode(potentials=logits_test,
                                                 transition_params=transition_params_test,
                                                 sequence_length=input_length_test)
        measures, lab_measures = metrics(X_test_batch,
                                         y_test_batch,
                                         batch_pred_sequence_test,
                                         configs,
                                         data_manager,
                                         tokenizer,
                                         mode='val',
                                         level=configs.measuring_metrics_level)

        for k, v in measures.items():
            test_results[k] += v
        for lab in lab_measures:
            for k, v in lab_measures[lab].items():
                test_labels_results[lab][k] += v

    time_span = (time.time() - start_time) / 60
    test_res_str = ''
    for k in test_results.keys():
        test_results[k] /= num_test_iterations
        test_res_str += (k + ': %.3f ' % test_results[k])
    for label, content in test_labels_results.items():
        test_label_str = ''
        for k in content.keys():
            test_labels_results[label][k] /= num_test_iterations
            test_label_str += (k + ': %.3f ' % test_labels_results[label][k])
        logger.info('label: %s, %s' % (label, test_label_str))
    logger.info('time consumption:%.2f(min), %s' % (time_span, test_res_str))
