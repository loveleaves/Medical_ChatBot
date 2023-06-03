# -*- coding: utf-8 -*-
import copy
import tensorflow as tf
from abc import ABC
from tensorflow_addons.text.crf import crf_log_likelihood, crf_decode
from transformers import TFBertModel, BertConfig


class Bert_BiLSTM_CRF_MODEL(tf.keras.Model):
    """
    function: BERT-BiLSTM-CRF
    other: inherit ABC(Abstract base class) class: Bert_BiLSTM_CRF_MODEL(tf.keras.Model, ABC)
        purpose:
            1. large function design or
            2. provide a common interface for different implementations of a component
        Note:
            The method's name must match the name of the ABC's method
    """
    def __init__(self, bert_path, configs, num_classes):
        super(Bert_BiLSTM_CRF_MODEL, self).__init__()
        # self.config = BertConfig.from_pretrained(bert_path)
        self.bert = TFBertModel.from_pretrained(bert_path)
        # self.Bert_BiLSTM_Model = tf.keras.models.load_model(model_path)
        self.bert.trainable = False
        self.hidden_dim = configs.hidden_dim
        self.dropout_rate = configs.dropout
        self.num_classes = num_classes
        self.dropout = tf.keras.layers.Dropout(self.dropout_rate)
        self.bilstm = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(self.hidden_dim, return_sequences=True))
        self.dense = tf.keras.layers.Dense(num_classes)
        self.transition_params = tf.Variable(tf.random.uniform(shape=(self.num_classes, self.num_classes)))
        # START_TAG = "<START>" # beginning of a sentence or specified text
        # STOP_TAG = "<STOP>" # ending of a sentence or specified text
        # self.transitions.data[tag_to_ix[START_TAG], :] = -10000  # any tag -> START_TAG : impossible
        # self.transitions.data[:, tag_to_ix[STOP_TAG]] = -10000  # STOP_TAG -> any tag : impossible
        self._set_inputs(tf.TensorSpec(shape=[None, 512], dtype=tf.int32, name='input_ids'))

    @tf.function(input_signature=[[tf.TensorSpec(shape=[None, 512], dtype=tf.int32, name='input_ids'),
                                  tf.TensorSpec(shape=[None], dtype=tf.int64, name='input_length'),
                                  tf.TensorSpec(shape=[None, 512], dtype=tf.int32, name='targets')]])
    def call(self, inputs):
        input_ids, input_length, targets = inputs
        embedding_outputs = self.bert(input_ids)
        """
        bert has a total of four outputs:
            last hidden state: shape:(batch_size, sequence_length, hidden_size)
            pooler_output: shape:(batch_size, hidden_size), 
                is the hidden state of the last layer of the first token (cls) of the sequence
            hidden_states(config.output_hidden_states=True needed): shape:(batch_size, sequence_length, hidden_size)
                a tuple includes 13 elements, outputs of every hidden layer
            attentions(config.output_attentions=True needed): shape:(batch_size, layer_nums, sequence_length, sequence_legth)
                a tuple includes 12 elements, attention weights of every layer
        """
        sequence_outputs = embedding_outputs[0]
        dropout_outputs = self.dropout(sequence_outputs)
        bilstm_outputs = self.bilstm(dropout_outputs)
        logits = self.dense(bilstm_outputs)
        tensor_targets = tf.convert_to_tensor(targets, dtype=tf.int32)
        log_likelihood, self.transition_params = crf_log_likelihood(logits,
                                                                    tensor_targets,
                                                                    input_length,
                                                                    transition_params=self.transition_params)
        """
        purpose: computes the log-likelihood of tag sequences in a CRF
        :param (4 elements): 
            inputs: shape:(batch_size, max_seq_len, num_tags)
            tag_indices: shape:(batch_size, max_seq_len)
            sequence_lengths: shape:(batch_size)
            transition_params: shape:(num_tags, num_tags)
        :return
            log_likelihood: log-likelihood, shape:scalar
            transition_params: transition matrix, shape:(num_tags, num_tags)
        """
        # update transition matrix
        # transition_params = self.transition_params
        return logits, log_likelihood, self.transition_params
