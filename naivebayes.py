import sys
import os
import preprocess
import bayesclassifier


GLOBAL = {} 
GLOBAL['dataCollection'] = sys.argv[1] if len(sys.argv) >= 2 else "fakenews/"
GLOBAL['BayesClassifier'] = []


def uniqueWordsInPost(post):
  uniqueWords = set()
  for line in post:
    uniqueWords.update(line)
  return uniqueWords

def prepInputDataset(folder, fileNames, readLabels = True):
  labels = set()
  data = []
  index = 0

  for file in fileNames:
    if "fake" not in file and "true" not in file:
      continue

    if readLabels == True:
      label = file[0:4]
      labels.add(label)
    
    words = []
    with open(folder + file, encoding = "iso-8859-1") as f:
      lines = f.readlines()
      for line in lines:
        line = line.strip().rstrip("\n")
        words.append(preprocess.tokenizeText(line))
      words = uniqueWordsInPost(words)
      data.append([x for x in words])
      data[index].append(label)
      index += 1
      f.close()
      
  return data, labels

def trainNaiveBayes(fileNames, folder):
  data, labels = prepInputDataset(folder, fileNames)
  GLOBAL['BayesClassifier'] = bayesclassifier.BayesClassifier()
  classifier = GLOBAL['BayesClassifier']
  return classifier.train(data, labels)

def testNaiveBayes(fileName, folder):
  classifier = GLOBAL['BayesClassifier']

  fileNames = []
  fileNames.append(fileName)

  testData, testClass = prepInputDataset(folder, fileNames)  
  predictedClass = classifier.predict(testData, testClass)

  with open('naivebayes.output.' + folder[0:len(folder) - 1], 'a') as outputFile:
    outputFile.write("%-15s %s\n" %(fileName, predictedClass))
    outputFile.close()

  return predictedClass, testClass

if __name__ == "__main__":
  folder =  GLOBAL['dataCollection']
  folder = folder if folder[-1] == '/' else folder + '/'
    
  fileNames = os.listdir(folder)
  fileNames.sort()

  with open('naivebayes.output.' + folder[0:len(folder) - 1], 'w') as outputFile:
    outputFile.close()

  leaveIndexOut = 0
  correctLabels = 0
  for i in range(len(fileNames)):
    if "fake" not in fileNames[leaveIndexOut] and "true" not in fileNames[leaveIndexOut]:
      leaveIndexOut = leaveIndexOut + 1
      continue

    fileNamesForTraining = fileNames[:leaveIndexOut] + fileNames[leaveIndexOut + 1:]
    classLogProbabilities, wordConditionalProbabilities = trainNaiveBayes(fileNamesForTraining, folder)
    predictedClass, testClass = testNaiveBayes(fileNames[leaveIndexOut], folder)

    if predictedClass in testClass:
      correctLabels = correctLabels + 1

    leaveIndexOut = leaveIndexOut + 1

  accuracy = float(correctLabels) / len(fileNames)

  print("correct labels %d " %(correctLabels))
  print("accuracy %f " %(accuracy))

  classifier = GLOBAL['BayesClassifier']
  sortedWordsByConditionalProbabilitiesTrue, sortedWordsByConditionalProbabilitiesFake = classifier.topWords()

  print("top 10 words for class true")
  count = 1
  for word, probability in sortedWordsByConditionalProbabilitiesTrue.items():
    print("%s probability %f" %(word, probability))
    if count == 10:
      break
    count += 1

  print("\ntop 10 words for class fake")
  count = 1
  for word, probability in sortedWordsByConditionalProbabilitiesFake.items():
    print("%s probability %f" %(word, probability))
    if count == 10:
      break
    count += 1