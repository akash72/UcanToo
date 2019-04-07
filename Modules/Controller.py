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
    wordRatio, wordQ, wordIdx = IdfMatch.getAnswer(QDict, question)
    answers = []
    answers.append(ADict[wordIdx])
    print("Time1: ", time.time() - startTime1, "Time2", time.time() - startTime2)
    return jsonify({
                    "question": question, 
                    "answers": answers, 
                    "ratio": wordRatio*10,
                    "closestQuestion": wordQ
                    })
    

# @app.route('/empdb/employee',methods=['GET'])
# def getAllEmp():
#     return jsonify({'emps':empDB})


# @app.route('/empdb/employee/<empId>',methods=['GET'])
# def getEmp(empId):
#     usr = [ emp for emp in empDB if (emp['id'] == empId) ] 
#     return jsonify({'emp':usr})


# @app.route('/empdb/employee/<empId>',methods=['PUT'])
# def updateEmp(empId):
#     em = [ emp for emp in empDB if (emp['id'] == empId) ]
#     if 'name' in request.json : 
#         em[0]['name'] = request.json['name']
#     if 'title' in request.json:
#         em[0]['title'] = request.json['title']
#     return jsonify({'emp':em[0]})


# @app.route('/empdb/employee',methods=['POST'])
# def createEmp():
#     dat = {
#     'id':request.json['id'],
#     'name':request.json['name'],
#     'title':request.json['title']
#     }
#     empDB.append(dat)
#     return jsonify(dat)


# @app.route('/empdb/employee/<empId>',methods=['DELETE'])
# def deleteEmp(empId):
#     em = [ emp for emp in empDB if (emp['id'] == empId) ]
#     if len(em) == 0:
#        abort(404)
#     empDB.remove(em[0])
#     return jsonify({'response':'Success'})
if __name__ == '__main__':
 app.run()
