# coding=utf-8
import keras
from knowledge_extraction.bilstm_crf.crf_layer import CRF


class BiLstmCrfModel(object):
    def __init__(
            self,
            max_len,
            vocab_size,
            embedding_dim,
            lstm_units,
            class_nums,
            embedding_matrix=None
    ):
        super(BiLstmCrfModel, self).__init__()
        self.max_len = max_len  # 截长补短
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.lstm_units = lstm_units
        self.class_nums = class_nums
        self.embedding_matrix = embedding_matrix
        if self.embedding_matrix is not None:
            self.vocab_size, self.embedding_dim = self.embedding_matrix.shape

    def build(self):
        inputs = keras.layers.Input(
            shape=(self.max_len,),  # (height,width,chanel)
            dtype='int32'
        )  # shape =[batch_size,max_len], img shape = [batch_size,height,width,chanel] #[2,5,1,4,0,0]
        # x = keras.layers.Masking(
        #         mask_value=0
        #     )(inputs)
        x = keras.layers.Embedding(
            input_dim=self.vocab_size,
            output_dim=self.embedding_dim,
            trainable=True,
            weights=self.embedding_matrix,
            mask_zero=True
        )(inputs)  # shape=[batch_size,max_len,embedding_dim] # [[0.12,0.231,...],[5],1,4,0,0]
        x = keras.layers.Bidirectional(
            keras.layers.LSTM(
                self.lstm_units,
                return_sequences=True  # False shape=[batch_size,lstm_units*2]
            )
        )(x)  # shape=[batch_size,max_len,lstm_units*2]
        x = keras.layers.TimeDistributed(
            keras.layers.Dropout(
                0.2
            )
        )(x)
        crf = CRF(self.class_nums)
        outputs = crf(x)
        model = keras.Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer='adam',
            loss=crf.loss_function,
            metrics=[crf.accuracy]
        )
        print(model.summary())

        return model, crf
