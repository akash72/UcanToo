# -*- encoding:utf-8 -*-
from __future__ import print_function

import sys,os
import numpy as np
import pickle
import argparse
import pandas as pd
import keras
import string
import itertools
import operator
import math

from decimal import *
from scipy import spatial
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pathlib import Path
from nltk.stem import WordNetLemmatizer
import tensorflow as tf


def openEmbeddingFile():

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    embedding_file = os.path.join(fileDir, 'Data/glove.840B.300d.txt')

    #Check if the embeddings file is already there
    embedFile = os.path.join(fileDir, 'Data/embeddings.pkl')
    if os.path.isfile(embedFile):
      print("GloVe embedding pickle found! Loading...")
      # file exists
      embeddings = pickle.load(open(embedFile, 'rb'))
      return embeddings

    # Get the embeddings
    print('Now creating word embedding vectors...')

    embeddings_index = {}
    f = open(embedding_file, 'r')
    for line in f:
        values = line.split()
        word = values[0]
        try:
            coefs = np.asarray(values[1:], dtype='float32')
        except ValueError:
            continue
        embeddings_index[word] = coefs

    print('Dumping vectors to file...')
    pickle.dump(embeddings_index, open("Data/embeddings.pkl", "wb"), protocol=-1)
    return embeddings_index


def generateStringEmbedding(in_str, embeddings):

    ctx_emb = np.zeros(300)

    # Add up the word embeddings
    for i, word in enumerate(in_str):
        emb_vec = embeddings.get(word)
        if emb_vec is not None:
            ctx_emb = np.add(emb_vec,ctx_emb)
    return ctx_emb

def generateQADict(embeddings):
    # Generate Glove embeddings for training questions with valid responses
    embedding_size = 300

    # Check if Dict exists
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    embedFile = os.path.join(fileDir, 'Data/QADict.pkl')
    if os.path.isfile(embedFile):
      print("QADict pickle found! Loading...")
      # file exists
      QADict = pickle.load(open(embedFile, 'rb'))
      return QADict

    print("Loading training files")
    # Load the train csv
    train = pd.read_csv('Data/train.csv')
    tr_ctxt, tr_rsp, tr_lbl = pickle.load(open('Data/train.pkl', mode="rb"))

    rows = train.shape[0]
    QADict = {}

    for i in range(rows):
        if (i % 1000) == 0:
            print("Process rows: ",i)
        # Save off the positive contexts
        if (train.loc[i].Label == 1):
            #Generate embedding for Context
            embedding = generateStringEmbedding(train.loc[i].Context, embeddings)
            # Save the following:
            # [0] The GloVe embedding for the question
            # [1] The tokenized response (to be fed into the ML model)
            # [2] The unlemmatized response string (to be returned to the user)
            QADict[i] = (embedding, tr_rsp[i], train.loc[i].Utterance)

    print("\nSaving training embeddings...")
    pickle.dump(QADict, open("Data/QADict.pkl", 'wb'), protocol=-1)
    return QADict

def lemmatizeInput(str):
    lemmatizer = WordNetLemmatizer() 

    str.translate(str.maketrans('', '', string.punctuation))
    words = str.split()
    lemmatizedString = ""
    for word in words:
        lemmatizedString += lemmatizer.lemmatize(word) + " "
    return lemmatizedString[:-1]

def euclidean_dist(x, y):
    return math.sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

def nth_root(value, n_root):
    root_value = 1 / float(n_root)
    return round(Decimal(value) ** Decimal(root_value), 3)

def minkowski_dist(x, y, p_value):
    return nth_root(math.sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)
   
def getResponse(input_string, embeddings, QADict, ucantoo_model, graph, tokenizer):

    # Current flow is as follows:
    # 1. Lemmatize input string and convert to a Glove vector
    # 2. Find the 10 closest question vectors to input string (diff the vectors)
    # 3. Save the tokenized responses correlated to these strings
    # 4. Tokenize the input string
    # 5. Call the predict function on the model
    # 6. Take the 'best' and return the unlemmatized version of response

    input_string = lemmatizeInput(input_string)

    #1. Convert input string to GloVe vector
    print("Generating input string embedding...")
    in_emb = generateStringEmbedding(input_string, embeddings)

    #2. Find the 10 best embedding matches and save the responses
    max_val = 100000
    respSeq = []

    respSen = []
    values = []
    dictValue = {}
    for entry in QADict:
        
        # Euclidean Distance between the two embeddings
        val = euclidean_dist(in_emb,QADict[entry][0])
        #minkowski Distance between the two embeddings
        # 3 is the order of the norm of the difference
        #val = minkowski_dist(in_emb,QADict[entry][0],3)
        # Cosine similarity between two vectors
        #val = 1 - spatial.distance.cosine(in_emb,QADict[entry][0])
        # Diff of the two embeddings
        #val = np.absolute(np.sum(np.subtract(in_emb, QADict[entry][0])));
        
        if len(values) < 10:
            values.append(val)
            dictValue[entry] = val
        else:
            values.sort()
            if val < values[9]:

                lastVal = values[9]

                # Deleting the key with the max value
                del dictValue[max(dictValue.items(), key=lambda k: k[1])[0]]

                dictValue[entry] = val
                values = values[:-1]
                values.append(val)
    
    print("values: ", values)
    print("Dict values: ", dictValue)
    
    for key in dictValue:
        respSeq.append(QADict[key][1])
        respSen.append(QADict[key][2])


    #4. Tokenize the input/response strings
    inputStr = []
    for w in range(10):
        inputStr.append(input_string)
    tokenizer.fit_on_texts(inputStr)
    inputStr = tokenizer.texts_to_sequences(inputStr)
    inputStr = pad_sequences(inputStr, maxlen=160)
    inputStr = np.asarray(inputStr)
    respStr = np.asarray(respSeq)

    print("Input string sequence is:\n", inputStr)
    print("Response string sequence is:\n", respStr)
    #print(ucantoo_model)
    #5. Send input string and responses to predict
    
    with graph.as_default():
        pred = ucantoo_model.predict([inputStr, respStr])
        print(pred)
        #print("Prediction is:\n", pred);

        #6. Return the best response (unlemmatized)
        maxIdx = np.argmax(pred)

        print("Top index is :\n", maxIdx)
        print("Resp: ", respSeq[maxIdx])
        return pred[maxIdx], respSen[maxIdx].replace("__eou__", '\n')