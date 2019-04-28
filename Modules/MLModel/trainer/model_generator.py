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

    # Create our dual encoder LSTM model
    hidden_sz = 300
    emb_sz = 300
    emb_file = 'glove.840B.300d.txt'

    print('Now indexing word vectors...')

    # Create the embedding vectors
    emb_idx = {}
    with file_io.FileIO(job_dir + emb_file, mode='r') as f:
        for line in f:
            val = line.split()
            word = val[0]
            try:
                wd_vec = np.asarray(values[1:], dtype='float32')
            except ValueError:
             continue
            emb_idx[word] = wd_vec
   
    # Load the parameters of our tokenized words from the train/dev/test set (keras preprocessed)
    max_seq_len, max_word_len, word_idx = pickle.load(file_io.FileIO(job_dir + 'params.pkl', mode="r"))

    print("Now generating embedding vector...")
    num_words = min(max_word_len, len(word_idx)) + 1
    emb_vec = np.zeros((num_words , emb_sz))
    for word, i in word_idx.items():
        if i >= max_word_len:
            continue
        emb = emb_idx.get(word)
        if emb is not None:
            # words not found in embedding index will be all-zeros.
            emb_vec[i] = emb

    print("Now building dual encoder lstm model...")
    # Define the lstm encoder
    encoder = Sequential()
    encoder.add(Embedding(output_dim=emb_sz,
                          input_dim=max_word_len,
                          input_length=max_seq_len,
                          weights=[emb_vec],
                          mask_zero=True,
                          trainable=True))
   
    # Add LSTM Layer
    encoder.add(LSTM(units=hidden_sz))
   
    # Define our inputs - both context and response sequence
    context_input = Input(shape=(max_seq_len,), dtype='int32')
    response_input = Input(shape=(max_seq_len,), dtype='int32')

    # Encode them
    context_branch = encoder(context_input)
    response_branch = encoder(response_input)
   
    # Multiply these together and add as the output
    concat = multiply([context_branch, response_branch])
    out = Dense((1), activation = "sigmoid") (concat)

    # Create the model
    model = Model([context_input, response_input], out)

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
    
    # Adding the TensorBoard callback
    tsboard = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
    
    print("Training the model...")
    ucantoo_model.fit([tr_ctxt, tr_rsp], tr_lbl,
        batch_size=bat_sz, epochs=eps, callbacks=[tsboard],
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
