# -*- coding:utf-8 -*-
import tensorflow as tf
import keras
import numpy as np
import os

from entity_normalization.esim import ESIM
from entity_normalization.data_helper import load_char_data, load_char_embed
from entity_normalization.config import esim_params, data_params

# np.random.seed(1)
# tf.set_random_seed(1)

if __name__ == '__main__':
    # char_embedding_matrix = load_char_embed(esim_params['max_features'],esim_params['embed_size'])
    # esim_params['embedding_matrix'] = char_embedding_matrix

    p, h, y = load_char_data(data_params['train_file'], data_size=None,
                             maxlen=esim_params['input_shapes'][0][0])
    x = [p, h]
    y = keras.utils.to_categorical(y, num_classes=esim_params['num_classes'])

    model = ESIM(esim_params).build()
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    print(model.summary())

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=4,
        verbose=2,
        mode='min'
    )
    best_model_filepath = esim_params['model_save_path']

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
        x=x,
        y=y,
        batch_size=32,
        epochs=6,
        validation_split=0.2,
        shuffle=True,
        callbacks=[earlystop, checkpoint]
    )

    model_frame_path = esim_params['model_frame_path']
    model_json = model.to_json()
    with open(model_frame_path, "w") as json_file:
        json_file.write(model_json)
