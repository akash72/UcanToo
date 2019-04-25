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
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pathlib import Path
from nltk.stem import WordNetLemmatizer


def openEmbeddingFile():

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    embedding_file = os.path.join(fileDir, 'Data/glove.840B.300d.txt');

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

    ctx_emb = np.zeros(300);

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
    embedFile = os.path.join(fileDir, 'Data/QADict.pkl');
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
            print("Process rows: ",i);
        # Save off the positive contexts
        if (train.loc[i].Label == 1):
            #Generate embedding for Context
            embedding = generateStringEmbedding(train.loc[i].Context, embeddings)
            # Save the following:
            # [0] The GloVe embedding for the question
            # [1] The tokenized response (to be fed into the ML model)
            # [2] The unlemmatized response string (to be returned to the user)
            QADict[i] = (embedding, tr_rsp[i], train.loc[i].Utterance)

    print("\nSaving training embeddings...");
    pickle.dump(QADict, open("Data/QADict.pkl", 'wb'), protocol=-1)
    return QADict

   
def getResponse(input_string, embeddings, QADict, ucantoo_model, tokenizer):

    # Current flow is as follows:
    # 1. Lemmatize input string and convert to a Glove vector
    # 2. Find the 10 closest question vectors to input string (diff the vectors)
    # 3. Save the tokenized responses correlated to these strings
    # 4. Tokenize the input string
    # 5. Call the predict function on the model
    # 6. Take the 'best' and return the unlemmatized version of response

    ## FIXME! - Need to lemmatize intput string
    #1. Lemmatize the string here

    #1. Convert input string to GloVe vector
    print("Generating input string embedding...");
    in_emb = generateStringEmbedding(input_string, embeddings);

    # FIXME! - Update to get 10 best
    #2. Find the 10 best embedding matches and save the responses
    max_val = 100000;
    respSeq = []

    # for entry in QADict:
    #     # Diff of the two embeddings
    #     val = np.absolute(np.sum(np.subtract(in_emb, QADict[entry][0])));
    #     if val < max_val:
    #         print("Val: ",val);
    #         max_val = val;
    #         #3. Save tokenized sequence for this response
    #         respSeq = (QADict[entry][1]);

    values = []
    dictValue = {}
    for entry in QADict:
        # Diff of the two embeddings
        val = np.absolute(np.sum(np.subtract(in_emb, QADict[entry][0])));

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

    print("Response seq: ", len(respSeq))

    #print("Best val: ", max_val);

    #4. Tokenize the input/response strings
    inputStr = []
    respStr = []
    inputStr.append(input_string);
    respStr.append(respSeq);
    tokenizer.fit_on_texts(inputStr);
    inputStr = tokenizer.texts_to_sequences(inputStr);
    inputStr = pad_sequences(inputStr, maxlen=160);
    inputStr = np.asarray(inputStr);
    respStr = np.asarray(respStr);

    print("Input string sequence is:\n", inputStr);
    print("Response string sequence is:\n", respStr);

    #5. Send input string and responses to predict
    pred = ucantoo_model.predict([inputStr, respStr]);

    #FIXME! - Find the highest prediction value
    print("Prediction is:\n", pred);
    print("Returning response:\n", best_resp[2]);
    #6. Return the best response (unlemmatized)
    return best_resp[2];


def lemmatizeInput(str):
    lemmatizer = WordNetLemmatizer() 

    str.translate(str.maketrans('', '', string.punctuation))
    words = str.split()
    lemmatizedString = ""
    for word in words:
        lemmatizedString += lemmatizer.lemmatize(word) + " "
    return lemmatizedString[:-1]

# Main entry point
if __name__ == "__main__":

    # Load/Generate the GloVe embeddings file
    embeddings = openEmbeddingFile();

    # Load/Generate QA Dictionary file
    QADict = generateQADict(embeddings);

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

    # Load the tokenizer (to tokenize the input string)
    with open('Data/tokenizer.pkl', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Get input string from user
    inStr = input("Ask an Ubuntu Question: ");
    
    # Magic!
    response = getResponse(lemmatizeInput(inStr), embeddings, QADict, ucantoo_model, tokenizer);

