#IDF String Matching
import math
import re
from flask import Flask
# from flask_caching import Cache

# cache = Cache(config={'CACHE_TYPE': 'simple',
#                       'CACHE_DEFAULT_TIMEOUT': 500000
#                      })
                     
# app = Flask(__name__)
# cache.init_app(app)

def getAnswer(QDict, question):
  return wordMatchIdf(question, QDict, genQIdfData(QDict))

def genQIdfData(QDict):

  # Generate IDF values for all words
  QIdfDict = {}

  N = len(QDict)

  for key in QDict:
    # print(QDict[key])
    # Tokenize each question string
    words = QDict[key][0].split()
    words = [x.lower() for x in words]

    for word in words:
      #strip html stuff out too
      word = re.sub(r'[<*>.,!;]','',word)

      if word in QIdfDict:
        QIdfDict[word] += 1
      else:
        QIdfDict[word] = 1

  for word in QIdfDict:
    QIdfDict[word] = math.log10(N/float(QIdfDict[word]))
    #print(word)
    #print(QIdfDict[word])
    #print("\n")

  # Normalize values
  maxKey = max(QIdfDict, key = lambda x: QIdfDict.get(x))
  minKey = min(QIdfDict, key = lambda x: QIdfDict.get(x))
  maxVal = QIdfDict[maxKey]
  minVal = QIdfDict[minKey]
  #print("maxVal: ",maxVal);
  #print("minVal: ",minVal);
  # z = x - min/(max - min)
  for word in QIdfDict:
    QIdfDict[word] = (QIdfDict[word] - minVal)/(maxVal - minVal)

  return QIdfDict

def wordMatchIdf(inString, QDict, QIdfDict):

    # Tokenize input String
    words = inString.split()

    # make all lowercase
    words = [x.lower() for x in words]

    #print(words);
    incount = len(words)

    # Keep top 3 matching questions
    maxMatchVal = 0;
    minMatchVal = [0, 0, 0];
    maxMatches = [0, 0, 0];
    maxRatio = [0, 0, 0];
    maxIdxs = [0, 0, 0];
    maxQs = {};

    # Iterate over Question Strings
    for key in QDict:
      # print(QDict[key])

      # Tokenize each question string
      curToken = QDict[key][0].split()

      matches = {x for x in words if x in curToken}

      matchVal = 0
      count = 0

      for word in matches:
          #print("Matched word: ", word)
          #print(QIdfDict[word])
          # Add IDF value to overall
          matchVal += QIdfDict[word]
          count += 1

      # See if this is top 3
      if(matchVal > min(minMatchVal)):
        #print("new matchVal is :", matchVal);
        # Get index
        idx = minMatchVal.index(min(minMatchVal));
        minMatchVal[idx] = matchVal;
        maxMatches[idx] = count;
        maxIdxs[idx] = QDict[key][1];
        maxQs[idx] = QDict[key][0];
        maxRatio[idx] = maxMatches[idx]/incount;


    # Sort the 3 values here
    maxIdx = minMatchVal.index(max(minMatchVal));
    minIdx = minMatchVal.index(min(minMatchVal));

    # Check if all the same value
    if maxIdx == minIdx:
        maxIdx = 0;
        minIdx = 2;

    # Find the medium value
    for i in range(3):
        if i != maxIdx and i != minIdx:
            medIdx = i

    #print("maxIdx: ",maxIdx);
    #print("minIdx: ",minIdx);
    #print("medIdx: ",medIdx);

    maxQuestions = {}
    maxRatios = [0, 0, 0]
    maxAIdxs = [0, 0, 0]
    maxQuestions[0] = maxQs[maxIdx]
    maxQuestions[1] = maxQs[medIdx]
    maxQuestions[2] = maxQs[minIdx]

    maxRatios[0] = maxRatio[maxIdx]
    maxRatios[1] = maxRatio[medIdx]
    maxRatios[2] = maxRatio[minIdx]

    maxAIdxs[0] = maxIdxs[maxIdx]
    maxAIdxs[1] = maxIdxs[medIdx]
    maxAIdxs[2] = maxIdxs[minIdx]

    #print("Input word count: ", count);
    #print("Matched word count: ", maxMatches);
    # FIXME! - Could use IDF ratio as better ratio
    
    print("maxQuestions: ", maxQuestions)
    print("maxRatios: ", maxRatios)
    print("maxAIdxs: ", maxAIdxs)

    return maxRatios, maxQuestions, maxIdxs
