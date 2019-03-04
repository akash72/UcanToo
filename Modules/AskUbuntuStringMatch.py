# String Matching Module

from difflib import SequenceMatcher


def loadQStrs(data):

  qDict = {};
  # Iterate over XML elements
  root_element = data.getroot()

  # Each element needs a Question ID, Question String, Answer ID
  QCount = 1;
  Unanswered = 0;
  ansArr = [];
  for child in root_element:
      type = int(child.get('PostTypeId'));
      # Only question types
      if(type == 1):
        QString = child.get('Body');
        AId = child.get('AcceptedAnswerId');

        # No unanswered questions
        if(AId is None):
            Unanswered = Unanswered + 1;
        else:
            if AId not in ansArr:
                ansArr.append(AId);
            qDict[QCount] = (QString, AId);
            #print(qDict[QCount]);
            QCount = QCount + 1;

  # Save off this dict for later
  #print (QCount)
  #print (Unanswered)
  print(len(ansArr))
  return qDict, ansArr;

def loadAStrs(data, ansArr):

     aDict = {};
     # Iterate over XML elements
     root_element = data.getroot()

     # Each element needs a Question ID, Question String, Answer ID
     ACount = 1;
     Unanswered = 0;
     for child in root_element:
         type = int(child.get('PostTypeId'));
         # Only answer types
         if(type == 2):
           AString = child.get('Body');
           AId = child.get('Id');
           # No unanswered questions
           if(AId is None):
               Unanswered = Unanswered + 1;
           elif AId in ansArr:
               aDict[AId] = (AString);
               #print(qDict[AId]);
               ACount = ACount + 1;

     # Save off this dict for later
     #print (ACount)
     #print (Unanswered)
     return aDict;

def compare(inString, QDict):

  # Iterate over Question Strings
  maxRatio = 0;
  maxIdx = 0;
  maxQ = "";

  for key in QDict:
    # print(QDict[key])

    # For each, generate the ratio value
    ratio = SequenceMatcher(None, inString, QDict[key][0], autojunk=True).ratio()
    # Save the max
    if(ratio > maxRatio):
      maxRatio = ratio;
      maxQ = QDict[key][0];
      maxIdx = QDict[key][1];

  return maxRatio, maxQ, maxIdx;
