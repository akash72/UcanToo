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

    # FIXME! - Compute total IDF for input words

    # Iterate over Question Strings
    maxMatchVal = 0
    maxMatches = 0
    maxIdx = 0
    maxQ = ""

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

      # Save the max
      if(matchVal > maxMatchVal):
        maxMatchVal = matchVal
        maxMatches = count
        #print("Max match val is :", maxMatchVal);
        #print("Max match count is :", maxMatches);
        maxQ = QDict[key][0]
        maxIdx = QDict[key][1]


    #print("Input word count: ", count);
    #print("Matched word count: ", maxMatches);
    # FIXME! - Could use IDF ratio as better ratio
    maxRatio = maxMatches/incount

    return maxRatio, maxQ, maxIdx
