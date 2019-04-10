#!/usr/bin/python

import AskUbuntuStringMatch as StringMatch
import AskUbuntuStringIdfMatch as IdfMatch
import sys, os
import _pickle as pickle
import gzip
from xml.etree import ElementTree as ET

def main(argv):

    datafile = sys.argv[1];

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    qfilename = os.path.join(fileDir, '../Data/ubuntuQDict.txt.gz');
    qidffilename = os.path.join(fileDir, '../Data/ubuntuQIdfDict.txt.gz');
    afilename = os.path.join(fileDir, '../Data/ubuntuADict.txt.gz');
    dfilename = os.path.join(fileDir, datafile);

    # Check for the saved dictionaries
    if (os.path.exists(qfilename) == True):
        print("Question Dict found! Loading...")
        # Load our Question dictionary
        QDict = pickle.load(gzip.open(qfilename,'rb'));
    else:
        print("Question Dict NOT found! Creating...")
        #Open the dataFile
        data = ET.parse(dfilename);
        #Get the questions
        QDict, ansArr = StringMatch.loadQStrs(data);
        # Save the questions
        with gzip.open(qfilename, 'wb') as f:
            f.write(pickle.dumps(QDict))

    if (os.path.exists(afilename) == True):
        print("Answer Dict found! Loading...")
        # Load our Answer dictionary
        ADict = pickle.load(gzip.open(afilename, 'rb'));
    else:
        print("Answer Dict NOT found! Creating...")
        #Open the dataFile
        data = ET.parse(dfilename);
        #Get the questions
        QDict, ansArr = StringMatch.loadQStrs(data);
        #Get the answers
        ADict = StringMatch.loadAStrs(data, ansArr);
        # Save the answers
        with gzip.open(afilename, 'wb') as f:
                f.write(pickle.dumps(ADict))

    if (os.path.exists(qidffilename) == True):
        print("Question IDF Dict found! Loading...")
        # Load our Question IDF dictionary
        QIdfDict = pickle.load(gzip.open(qidffilename,'rb'));
    else:
        print("Question IDF Dict NOT found! Creating...")
        QIdfDict = IdfMatch.genQIdfData(QDict);
        # Save the Question IDF
        with gzip.open(qidffilename, 'wb') as f:
                f.write(pickle.dumps(QIdfDict))

    #Ask user for a question
    inStr = input("Ask an Ubuntu Question: ");

    #Pass question into compare
    #Should get index, matched question, and ratio values back
    # wordMatch
    ##wordRatio, wordQ, wordIdx = StringMatch.wordMatch(inStr, QDict);
    # wordIdfMatch
    wordRatios, wordQs, wordIdxs = IdfMatch.wordMatchIdf(inStr, QDict, QIdfDict);

    #Print everything out
    print("\nQuestion Asked: ",inStr);
    wordAns = {};
    #Get answer based on index
    for i in range(3):
      wordAns[i] = ADict[wordIdxs[i]];
      print("Showing Match Number: ", i+1);
      print("\nRatio: ", wordRatios[i]*100);
      print("\nQuestion Found: ",wordQs[i]);
      print("\nAnswer: ", wordAns[i]);

if __name__ == "__main__":
    #Argument one should be relative path to datafile (../Data/Posts.xml)
    main(sys.argv[1:]);
