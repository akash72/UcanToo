import AskUbuntuStringIdfMatch as IdfMatch
import AskUbuntuStringMatch as StringMatch
from flask import Flask
from flask import jsonify
from flask import request
import time

import sys, os
import _pickle as pickle
import gzip
from xml.etree import ElementTree as ET

app = Flask(__name__)
startTime1 = time.time()

def setConfig():

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    # Check for the Q/A dict stored off
    qfilename = os.path.join(fileDir, '../Data/ubuntuQDict.txt.gz')
    afilename = os.path.join(fileDir, '../Data/ubuntuADict.txt.gz')
    dfilename = os.path.join(fileDir, "test_string")

    if (os.path.exists(qfilename) == True and
       os.path.exists(afilename) == True):
        print("Question/Answer Dicts found! Loading...")
        # Load our Question dictionary
        QDict = pickle.load(gzip.open(qfilename,'rb'))
        #QDict = pickle.load(open(qfilename, "rb"));
        # Load our Answer dictionary
        ADict = pickle.load(gzip.open(afilename, 'rb'))
        return QDict, ADict
    else:
        print("Question/Answer Dicts NOT found! Creating...")
        #Open the dataFile
        data = ET.parse(dfilename)
        #Get the questions
        QDict, ansArr = StringMatch.loadQStrs(data)
        # Save the questions
        with gzip.open(qfilename, 'wb') as f:
            f.write(pickle.dumps(QDict))

        #Get the answers
        ADict = StringMatch.loadAStrs(data, ansArr)
        # Save the answers
        with gzip.open(afilename, 'wb') as f:
                f.write(pickle.dumps(ADict))
        return QDict, ADict


QDict, ADict = setConfig()

@app.route('/askubuntu/questions', methods=['POST'])
def getAnswer():  
    startTime2 = time.time()
    question = request.json['question']
    ratios, questions, ids = IdfMatch.getAnswer(QDict, question)
    answers = []
    answers.append(ADict[ids[0]])
    answers.append(ADict[ids[1]])
    answers.append(ADict[ids[2]])


    print("Time1: ", time.time() - startTime1, "Time2", time.time() - startTime2)
    return jsonify({
                    "question": question, 
                    "answers": answers, 
                    #"ratio": wordRatio*10,
                    #"closestQuestion": wordQ
                    })
    


if __name__ == '__main__':
 app.run()
