# -*- encoding:utf-8 -*-
from __future__ import print_function

import numpy as np
import pickle
import argparse
import pandas as pd

def createEmbeddingFile():
    embedding_file = 'glove.840B.300d.txt'

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
    pickle.dump(embeddings_index, open("embeddings.pkl", "wb"), protocol=-1)


def generateStringEmbedding(in_str, embeddings):

    ctx_emb = np.zeros(300);

    # Add up the word embeddings
    for i, word in enumerate(in_str):
        emb_vec = embeddings.get(word)
        if emb_vec is not None:
            ctx_emb = np.add(emb_vec,ctx_emb)
    return ctx_emb

def generateEmbeddings():
## Generate Glove embeddings for training questions with valid responses
    embedding_size = 300

    # Load the train data with only true responses
    print("Loading word embeddings...")
    embeddings = pickle.load(open('embeddings.pkl', 'rb'))

    print("Loading training file")
    # Load the train csv
    train = pd.read_csv('train.csv')
    rows = train.shape[0]
    context = []
    response = []
    for i in range(rows):
        if (i % 1000) == 0:
            print("Process rows: ",i);
        # Save off the positive contexts
        if (train.loc[i].Label == 1):
            #Generate embedding for Context
            embedding = generateStringEmbedding(train.loc[i].Context, embeddings)
            context.append(embedding)
            # Save the lemmatized response
            response.append(train.loc[i].Utterance)

    print("Saving training embeddings...");
    pickle.dump([context, response], open("contexts.pkl", 'wb'), protocol=-1)

   
def getResponse(input_string):

    # Current flow is as follows:
    # 1. Lemmatize input string and convert to a Glove vector
    # 2. Load a file that has Questions (with label=1) that are converted to Glove vector
    # 3. Find the 10 closest to input string (diff the vectors)
    # 4. Take the lemmatized responses correlated to these strings and tokenize for keras
    # 5. Call the predict function on the model
    # 6. Take the 'best' and return the unlemmatized version of response

    print("Loading word embeddings...");
    ## FIXME! - Need to keep these open for performance
    # Load the word embeddings
    embeddings = pickle.load(open('embeddings.pkl', 'rb'))

    print("Generating input string embedding...");
    ## FIXME! - Need to lemmatize intput string
    # Generate the embedding for the input string
    in_emb = generateStringEmbedding(input_string, embeddings);

    print("Loading context embeddings...");
    ## FIXME! - Need to keep these open for performance
    # Load the context embeddings
    context_embeddings,responses = pickle.load(open('contexts.pkl', 'rb'))

    ###################################
    ### TODO! Everything below here ###
    ###################################

    print("Loading lemmatized responses...");
    ## FIXME! - Need to keep these open for performance
    # Load the lemmatized responses
    
    print("Loading raw responses...");
    ## FIXME! - Need to keep these open for performance
    # Load the lemmatized responses

    # Find the 10 best embedding matches and save the responses
    max_val = 100000;
    best_resp_count = 0;
    best_resp = []

    for embedding,response in zip(context_embeddings,responses):
        # Diff of the two embeddings
        val = np.absolute(np.sum(np.subtract(in_emb, embedding)));
        if val < max_val:
            print("Val: ",val);
            # Add this response
            #best_resp.append(response);
            best_resp = response;
            max_val = val;
            best_resp_count = best_resp_count + 1;

            # Once we get 10, control

    print("Found # of responses: ", best_resp_count);
    print("Best val: ", max_val);
    print("Best response:\n", best_resp);
    # Send input string and responses to predict

    # Need to use Tokenizer to get it set correctly


# Main entry point
if __name__ == "__main__":

    # Create the file
    # FIXME! - Uncomment to generate embeddings file
    #createEmbeddingFile();

    # FIXME! - Uncomment to generate embeddings file
    #generateEmbeddings();

    # Get input string from user
    inStr = input("Ask an Ubuntu Question: ");

    response = getResponse(inStr);

