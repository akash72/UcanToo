# -*- encoding:utf-8 -*-
from __future__ import print_function

import sys,os
import numpy as np
import pickle
import argparse
import keras
import math
import string
import statistics
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pathlib import Path
from keras import backend as K
from nltk.stem import WordNetLemmatizer
import model_interface as modelInterface
import tensorflow as tf

# Main entry point
if __name__ == "__main__":

    # Load/Generate the GloVe embeddings file
    embeddings = modelInterface.openEmbeddingFile();

    # Load/Generate QA Dictionary file
    QADict = modelInterface.generateQADict(embeddings);

    # Load the ML model
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    json_file = os.path.join(fileDir, 'Data/model.json');
    model_json_file = open(json_file, 'r')
    loaded_model_json = model_json_file.read()
    model_json_file.close()
    ucantoo_model = model_from_json(loaded_model_json)

    # Load the ML model weights
    ucantoo_model.load_weights("Data/model.h5")

    print("Loaded model from disk")
 
    # Compile the model
    ucantoo_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    graph = tf.get_default_graph()

    # Load the tokenizer (to tokenize the input string)
    with open('Data/tokenizer.pkl', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    # Evaluate
    if len(sys.argv) > 1:

        print("Evaluate model...\n")
        # Load the test data
        test_sen, test_resp = pickle.load(open('Data/test_ten_sen.pkl', 'rb'))

        totVal = []
        # For each test context
        for i in range(10):
            print("Sending question: \n", test_sen[i]);
            val, response = modelInterface.getResponse(test_sen[i], embeddings, QADict, ucantoo_model, graph, tokenizer)
            print("predict val: \n", val);
            totVal.append(val);

        totVal = np.asarray(totVal);
        print("Max: ",max(totVal));
        print("Min: ",min(totVal));
        print("Avg: ",np.mean(totVal));
        print("Std Dev: ",np.std(totVal));
    else:

        # Get input string from user
        inStr = input("Ask an Ubuntu Question: ");

        # Magic!
        response = modelInterface.getResponse(inStr, embeddings, QADict, ucantoo_model, graph, tokenizer);


