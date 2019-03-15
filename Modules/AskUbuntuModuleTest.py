#!/usr/bin/python

import AskUbuntuStringMatch as StringMatch
import sys, os
import _pickle as pickle
import gzip
from xml.etree import ElementTree as ET

def main(argv):

    datafile = sys.argv[1];

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    # Check for the Q/A dict stored off
    qfilename = os.path.join(fileDir, '../Data/ubuntuQDict.txt.gz');
    afilename = os.path.join(fileDir, '../Data/ubuntuADict.txt.gz');
    dfilename = os.path.join(fileDir, datafile);

    if (os.path.exists(qfilename) == True and
       os.path.exists(afilename) == True):
        print("Question/Answer Dicts found! Loading...")
        # Load our Question dictionary
        QDict = pickle.load(gzip.open(qfilename,'rb'));
        #QDict = pickle.load(open(qfilename, "rb"));
        # Load our Answer dictionary
        ADict = pickle.load(gzip.open(afilename, 'rb'));
    else:
        print("Question/Answer Dicts NOT found! Creating...")
        #Open the dataFile
        data = ET.parse(dfilename);
        #Get the questions
        QDict, ansArr = StringMatch.loadQStrs(data);
        # Save the questions
        with gzip.open(qfilename, 'wb') as f:
            f.write(pickle.dumps(QDict))

        #Get the answers
        ADict = StringMatch.loadAStrs(data, ansArr);
        # Save the answers
        with gzip.open(afilename, 'wb') as f:
                f.write(pickle.dumps(ADict))

    #Ask user for a question
    inStr = input("Ask an Ubuntu Question: ");

    #Pass question into compare
    #Should get index, matched question, and ratio values back
    wordRatio, wordQ, wordIdx = StringMatch.wordMatch(inStr, QDict);
    #Get answer based on index
    wordAns = ADict[wordIdx];

    #Print everything out
    print("\nQuestion Asked: ",inStr);
    print("Ratio: ", wordRatio*100);
    print("Closest Question Found (Word): ",wordQ);
    print("Answer: ", wordAns);

if __name__ == "__main__":
    #Argument one should be relative path to datafile (../Data/Posts.xml)
    main(sys.argv[1:]);
