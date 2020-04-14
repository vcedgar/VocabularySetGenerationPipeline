from DocumentModel.Sentence import Sentence
import math
import spacy
from spacy.lang.en import English
from pathlib import Path

class Document:
    def __init__(self, text, student):
        self.unknownWords = {}
        self.easyWords = {}
        self.difficultWords = {}
        self.student = student
        self.spacyDoc = self.loadSpacyDoc(text)

        # Getting the average length of the sentences. BERT will be configured to use this length time 2.5 for the token length
        spacySents = self.spacyDoc.sents
        lengthOfSents = 0
        numOfSents = 0
        for sent in spacySents:
            lengthOfSents += len(sent)
            numOfSents += 1
        avgLenOfSents = lengthOfSents / numOfSents
        Sentence.staticSentenceMaxTokens = math.floor(avgLenOfSents*2.5)

        spacySents = self.spacyDoc.sents
        self.sents = []
        self.numMasked = 0
        for sent in spacySents:
            try:
                newSent = Sentence(sent, student)
                self.numMasked += newSent.numMasked
                self.sents.append(newSent)
            except Exception:
                # if the sentence contains too many tokens break it into small ones
                division = math.ceil((len(sent) * 2) / Sentence.staticSentenceMaxTokens)
                start = 0
                end = math.floor(Sentence.staticSentenceMaxTokens/2)
                for j in range(0, division):
                    newSent = Sentence(sent[start: end], student)
                    self.numMasked += newSent.numMasked
                    self.sents.append(newSent)
                    start += math.floor(Sentence.staticSentenceMaxTokens/2)
                    end += math.floor(Sentence.staticSentenceMaxTokens/2)

        self.numMaskedPredicted = 0

    def predictDocument(self):
        for sent in self.sents:
            self.student.predict(sent)
            self.numMaskedPredicted += sent.numMaskedPredicted

    def organaizeVocab(self):
        self.unknownWords = {}
        self.easyWords = {}
        self.difficultWords = {}

        for sent in self.sents:
            for word in sent.words:
                if word.isMasked:
                    if word.lemma in self.unknownWords:
                        self.unknownWords[word.lemma].append(word)
                    else:
                        self.unknownWords[word.lemma] = [word]

        for lemma in self.unknownWords.keys():
            predicted = False
            # doing this to account for multiple instances of the same word
            for word in self.unknownWords[lemma]:
                if word.predicted:
                    predicted = True
            if predicted:
                self.easyWords[lemma] = self.unknownWords[lemma]
            else:
                self.difficultWords[lemma] = self.unknownWords[lemma]

    """Unmasks vocabulary that was predicted useful for further predictions"""
    def unmaskVocab(self):

        for lemma in self.easyWords.keys():
            wordList = self.easyWords[lemma]
            for word in wordList:
                word.unmask()
        for sent in self.sents:
            sent.unmask()

    def loadSpacyDoc(self, text):
        spacy.prefer_gpu()
        lang = English()
        sentencizer = lang.create_pipe("sentencizer")
        spacyNlp = spacy.load("en_core_web_lg")
        spacyNlp.add_pipe(sentencizer, before="parser")

        # Create SpaCy document for sentencizing and lemmatizing
        spacyDoc = spacyNlp(text)
        return spacyDoc

