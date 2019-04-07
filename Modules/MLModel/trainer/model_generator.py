# -*- encoding:utf-8 -*-
from __future__ import print_function

import numpy as np
import pickle
import tensorflow as tf
import keras
from keras.models import Sequential, Model
from keras.utils import np_utils
from keras.layers import Dense, Input, LSTM, multiply, Embedding
from keras import callbacks
from tensorflow.python.lib.io import file_io
import argparse

def model(job_dir):

    hidden_size = 300
    embedding_size = 300
    embedding_file = 'glove.840B.300d.txt'

    print('Now indexing word vectors...')

    # Load the embedding vectors
    embeddings_index = {}
    with file_io.FileIO(job_dir + embedding_file, mode='r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            try:
                coefs = np.asarray(values[1:], dtype='float32')
            except ValueError:
             continue
            embeddings_index[word] = coefs
   
    # Load the parameters of our tokenized words from the train/dev/test set (keras preprocessed)
    MAX_SEQUENCE_LENGTH, MAX_NB_WORDS, word_index = pickle.load(file_io.FileIO(job_dir + 'params.pkl', mode="r"))

    print("MAX_SEQUENCE_LENGTH: {}".format(MAX_SEQUENCE_LENGTH))
    print("MAX_NB_WORDS: {}".format(MAX_NB_WORDS))
    
    print("Now loading embedding matrix...")
    num_words = min(MAX_NB_WORDS, len(word_index)) + 1
    embedding_matrix = np.zeros((num_words , embedding_size))
    for word, i in word_index.items():
        if i >= MAX_NB_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    print("Now building dual encoder lstm model...")
    # define lstm encoder
    encoder = Sequential()
    encoder.add(Embedding(output_dim=embedding_size,
                            input_dim=MAX_NB_WORDS,
                            input_length=MAX_SEQUENCE_LENGTH,
                            weights=[embedding_matrix],
                            mask_zero=True,
                            trainable=True))
    
    encoder.add(LSTM(units=hidden_size))
    
    context_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    response_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')

    context_branch = encoder(context_input)
    response_branch = encoder(response_input)
    
    concatenated = multiply([context_branch, response_branch])
    out = Dense((1), activation = "sigmoid") (concatenated)

    model = Model([context_input, response_input], out)

    print(encoder.summary())

    return model


def main(job_dir,**args):

    #logs
    logs_path = job_dir + '/logs/'   

    optim = 'adam'
    bat_sz = 512
    eps = 1
    seed = 1348

    np.random.seed(seed)
 
    print("Starting...")

    ##Using the GPU
    #with tf.device('/device:GPU:0'): 

    # Call the model function
    ucantoo_model = model(job_dir)

    # Compile the model
    ucantoo_model.compile(loss='binary_crossentropy', optimizer=optim)
   
    # Print out a summary of the model
    print(ucantoo_model.summary())
   
    # Load the training, dev, test data
    tr_ctxt, tr_rsp, tr_lbl = pickle.load(file_io.FileIO(job_dir + 'train.pkl', mode="r"))
    tst_ctxt, tst_rsp, tst_lbl = pickle.load(file_io.FileIO(job_dir + 'test.pkl', mode="r"))
    dev_ctxt, dev_rsp, dev_lbl = pickle.load(file_io.FileIO(job_dir + 'dev.pkl', mode="r"))
    
    #print('%s train entries.' % len(tr_ctxt))
    #print('%s dev entries.' % len(dev_ctxt))
    #print('%s test entries.' % len(tst_ctxt))
    
    # Adding the TensorBoard callback
    tensorboard = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
    
    print("Training the model...")
    ucantoo_model.fit([tr_ctxt, tr_rsp], tr_lbl,
        batch_size=bat_sz, epochs=eps, callbacks=[tensorboard],
        validation_data=([dev_ctxt, dev_rsp], dev_lbl), verbose=1)

    # classify the test set
    #y_pred = ucantoo_model.predict([tst_ctxt, tst_rsp])          
        
    # Save model.h5 on to google storage
    print("Saving the model...")
    ucantoo_model.save('model2.h5')
    with file_io.FileIO('model2.h5', mode='r') as input_f:
        with file_io.FileIO(job_dir + '/model2.h5', mode='w+') as output_f:
            output_f.write(input_f.read())

# Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Input Arguments
    parser.add_argument(
      '--job-dir',
      help='GCS location to write checkpoints and export models',
      required=True
    )
    args = parser.parse_args()
    arguments = args.__dict__

    main(**arguments)                
