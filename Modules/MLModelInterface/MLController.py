from flask import Flask
from flask import jsonify
from flask import request

from keras.models import model_from_json
import model_interface as modelInterface
import sys, os
import _pickle as pickle
import gzip
import numpy as np
import tensorflow as tf

global ucantoo_model, graph

app = Flask(__name__)

# Load/Generate the GloVe embeddings file
embeddings = modelInterface.openEmbeddingFile()

# Load/Generate QA Dictionary file
QADict = modelInterface.generateQADict(embeddings)

# Load the ML model
fileDir = os.path.dirname(os.path.realpath('__file__'))
json_file = os.path.join(fileDir, 'Data/model.json')
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

@app.route('/ubuntuqa/questions', methods=['POST'])
def getAnswer():  
    
    question = request.json['question']
    val, response = modelInterface.getResponse(question, embeddings, QADict, ucantoo_model, graph, tokenizer)
    return jsonify({
                    "question": question, 
                    "answers": response, 
                    })

if __name__ == '__main__':
 app.run()