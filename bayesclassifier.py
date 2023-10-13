import math

class BayesClassifier:
  def init(self, data, labels):
    self.data = data
    self.labels = labels
    self.labelCounts = {}
    self.labelLogProbabilities = {}
    self.wordsPerLabelCount = {'': {}}
    self.wordsPerLabelLogProbabilities = {'': {}}
    self.uniqueWordsCount = {}
    self.posts = len(self.data)
    self.totalUniqueWords = 0

    for label in self.labels:
      self.labelCounts.setdefault(label, 0)
      self.labelLogProbabilities.setdefault(label, 0)

  def train(self, data, labels):
    self.init(data, labels)

    for row in self.data:
      self.labelCounts[row[-1]] = self.labelCounts[row[-1]] + 1
      self.labelLogProbabilities[row[-1]] = self.labelLogProbabilities[row[-1]] + 1

      for i in range(0, len(row) - 1):
        self.uniqueWordsCount.setdefault(row[i], 0)
        self.uniqueWordsCount[row[i]] = self.uniqueWordsCount[row[i]] + 1

        self.wordsPerLabelCount.setdefault(row[-1], {})
        self.wordsPerLabelCount[row[-1]].setdefault(row[i], 0)
        self.wordsPerLabelCount[row[-1]][row[i]] =  self.wordsPerLabelCount[row[-1]][row[i]] + 1

        self.wordsPerLabelLogProbabilities.setdefault(row[-1], {})
        self.wordsPerLabelLogProbabilities[row[-1]].setdefault(row[i], 0)
        self.wordsPerLabelLogProbabilities[row[-1]][row[i]] =  self.wordsPerLabelLogProbabilities[row[-1]][row[i]] + 1

    self.totalUniqueWords = len(self.uniqueWordsCount)

    for className, wordLikelihoodDictionary in self.wordsPerLabelLogProbabilities.items():
      for word, count in wordLikelihoodDictionary.items():
        wordLikelihoodDictionary[word] = math.log((count + 1)/ (2 + self.labelCounts[className]))

    for className, count in self.labelLogProbabilities.items():
      self.labelLogProbabilities[className] = math.log(count / self.posts)

    self.sortedWordsByConditionalProbabilitiesTrue = sorted(self.wordsPerLabelLogProbabilities['true'].items(), key=lambda x:x[1], reverse=True) 
    self.sortedWordsByConditionalProbabilitiesFake = sorted(self.wordsPerLabelLogProbabilities['fake'].items(), key=lambda x:x[1], reverse=True) 

    self.sortedWordsByConditionalProbabilitiesTrue = dict(self.sortedWordsByConditionalProbabilitiesTrue)
    self.sortedWordsByConditionalProbabilitiesFake = dict(self.sortedWordsByConditionalProbabilitiesFake)
    return self.labelLogProbabilities, self.wordsPerLabelLogProbabilities

  def predict(self, testData, testLabels):
    maxLikelihood = float('-inf')
    predictedClass = ''
    for className, classLogProbability in self.labelLogProbabilities.items():
      classLikelihood = classLogProbability

      for row in testData:
        for i in range(0, len(row) - 1):
          wordLogProbability = 0.0

          word = row[i]

          if word in self.wordsPerLabelLogProbabilities[className]:
            wordLogProbability = self.wordsPerLabelLogProbabilities[className][word]
          else:
            wordLogProbability = math.log(1 / (2 + self.labelCounts[className]))

          classLikelihood = classLikelihood + wordLogProbability

      if maxLikelihood < classLikelihood:
        maxLikelihood = classLikelihood
        predictedClass = className

    return predictedClass

  def topWords(self):
    return self.sortedWordsByConditionalProbabilitiesTrue, self.sortedWordsByConditionalProbabilitiesFake