import math
import random

def makeQuartileTest(vocab):
    count = len(vocab)
    wordsIn5Percent = math.ceil(count/20) - 1
    index = 0
    testList = []
    while index <= count - wordsIn5Percent:
        # find how what words are in the 1st, 2nd, etc 20%
        percent = vocab[index: index+wordsIn5Percent]
        # grab a random word from it
        print(wordsIn5Percent)
        wordIndex = random.randrange(0, wordsIn5Percent)
        testList.append(percent[wordIndex])
        index = index + wordsIn5Percent
    return testList

def makeVocabTests(vocab):
    count = len(vocab)
    if count < 80:
        return [], 0
    wordsInQuartile = math.ceil(count/4) - 1
    index = 0
    # make the quartile tests
    quartileTests = []
    while index <= count - wordsInQuartile:
        quartile = vocab[index: index+wordsInQuartile]
        quartileTest = makeQuartileTest(quartile)
        quartileTests.append(quartileTest)
        index = index + wordsInQuartile
    return quartileTests, wordsInQuartile

def calcQuartileTestResults(quartileTestResults):
    avg = 0
    total = 0
    wordsUnderstood = 0

    # To save known correct words regarrdless of frequency:
    words = []
    for word in quartileTestResults:
        total += 1
        # compute the rolling average of percent words known
        if quartileTestResults[word]:
            avg = (avg * (float(total) - 1) + 1)/float(total)
            words.append(word)
        else:
            avg = (avg * (float(total) - 1)) / float(total)

        # if the rolling average stays above 90%, we consider the unknown words outliers, this part of the section is known
        if avg >.90:
            wordsUnderstood = total
    # if the end rolling average was bellow 10%, we consider the known words outliers, the whole seciton is unknown
    if avg <= 0.1:
        wordsUnderstood = 0
    return wordsUnderstood, words

def calcTestsResults(quartileTestsResults, wordsInQuartile):
    quartiles = []
    wordsKnown = []
    index = 0
    quartNumb = 1
    for quartile in quartileTestsResults:
        correctCount, words = calcQuartileTestResults(quartile)
        print(correctCount)
        print(correctCount/20)
        numberWordsKnownInQuartile = int(wordsInQuartile*(correctCount/20))
        print("words knonw quartile", numberWordsKnownInQuartile)
        wordsKnown.extend(words)
        index += wordsInQuartile
        quartiles.append({"quartile": quartNumb, "wordsKnown": numberWordsKnownInQuartile})
        quartNumb += 1

    firstQuartile = 0
    lastQuartile = 3
    # discover which (if any) quartiles are completely known and unknown
    # That way we never test those sections again
    for i in range(3, 1, -1):
        if quartiles[i]["wordsKnown"] == 0:
            lastQuartile = i - 1
    for i in range(0, 2):
        if quartiles[i]["wordsKnown"] == wordsInQuartile:
            firstQuartile = i + 1

    # Figure out where in the earlier quartile the knowledge lies
    # figure out where in the later quartile the knowledge lies
    end = 0
    if(firstQuartile == lastQuartile):
        end = lastQuartile * wordsInQuartile
        start = firstQuartile * wordsInQuartile
    else:
        end = lastQuartile * wordsInQuartile + quartiles[lastQuartile]["wordsKnown"]
        start = firstQuartile * wordsInQuartile + quartiles[firstQuartile]["wordsKnown"]
    # start represents the last frequency level we believe without a doubt the student to be at
    # end represents the first frequency level after which we believe withoout a doubt the student is not at
    # in between we are unsure of
    return start, end, wordsKnown

def runVocabTest(vocab, levelOfGranularity):
    start = 0
    end = len(vocab)
    wordsKnown = []
    # Start and end get closer and closer as we go to lower levels of granularity.
    for i in range(0, levelOfGranularity):
        if start != end:
            vocabToTest = vocab[start:end]
            tests, wordsInQuartile = makeVocabTests(vocabToTest)
            if wordsInQuartile != 0:
                testsResults = []
                for test in tests:
                    result = runQuartileTest(test)
                    testsResults.append(result)
                newStart, newEnd, words = calcTestsResults(testsResults, wordsInQuartile)
                end = start + newEnd
                start += newStart
                wordsKnown.extend(words)

    # since start represents the end of where we are *sure* that the student has knowledge
    finalVocab = vocab[0:start]
    # wordsKnown contains words known by a the student regardless of frequency as result of the tests
    finalVocab.extend(wordsKnown)
    # gets rid of duplicates
    finalVocab = set(finalVocab)
    finalVocab = list(finalVocab)
    return finalVocab

def runQuartileTest(vocab):
    # To save known correct words regarrdless of frequency:
    results = {}
    for word in vocab:
        # Test each word
        uInput = input("Do you know this word: " + word)
        # compute the rolling average of percent words known
        if uInput == "y":
            results[word] = True
        else:
            results[word] = False
    print(results)
    return results

if __name__ == "__main__":
    vocabPath = "E:/User/Documents/PycharmProjects/VocabLessonGen/VocabularyFiles/lexique3_words_90_percentile.tsv"
    vocab = []
    with open(vocabPath, "r", encoding='utf8') as file:
        count = 0
        for line in file:
            if count == 0:
                pass
            info = line.split("\t")
            word = info[1]
            vocab.append(word)

    print(runVocabTest(vocab, 3))