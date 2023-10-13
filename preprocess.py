import re

def tokenizeText(inputString):
    textToSplit = "\s+"
    raw = re.split(textToSplit, inputString)
    output = []
    punctuation = ".!?,"
    for i, token in enumerate(raw):
        if "." in token and len(token) > 1:
            if isAcronym(token) or isAbbrev(token) or isNumber(token):
                pass
        elif "'" in token: 
            apostLoc = token.find("'")
            output.append(token[:apostLoc])
            token = token[apostLoc:]
        elif isDate(token):
            pass
        elif "-" in token: 
            pass
        else: 
            token = token.translate(str.maketrans('', '', punctuation))
        if token: 
            output.append(token)
    return output

def isAcronym(inputString):
    numberOfLetters = 0
    numberOfPeriods = 0
    if inputString.isupper():
        for ch in inputString: 
            if ch == ".":
                numberOfPeriods += 1
            elif ch.isalpha():
                numberOfLetters += 1
        if numberOfLetters == numberOfPeriods and numberOfLetters != 1: 
            return True
    return False

def isAbbrev(inputString):
    if len(inputString) <= 4:
        if inputString[len(inputString) - 1] == ".":
            return True
    return False

def isNumber(inputString):
    try:
        float(inputString)
        return True
    except ValueError:
        return False

def isDate(inputString):
    d1 = re.compile('(\d+)/(\d+)/(\d+)')
    d2 = re.compile('(\d+).(\d+).(\d+)')
    d3 = re.compile('(\d+)-(\d+)-(\d+)')
    candidate = d1.findall(inputString) or d2.findall(inputString) or d3.findall(inputString)
    if candidate:
        month, day, year = candidate[0]

        month = int(month)
        day = int(day)
        year = int(year)
   
        if 1 <= month <= 12 and 1 <= day <= 31 and 1000 <= year <= 3000:
            return True
   
        day, month, year = candidate[0]
   
        month = int(month)
        day = int(day)
        year = int(year)
   
        if 1 <= month <= 12 and 1 <= day <= 31 and 1000 <= year <= 3000:
            return True
    return False

