from DocumentModel.Word import Word

class Sentence:
    # This will be set at 3 * the average length of sentence
    # 64 is default
    staticSentenceMaxTokens = 64

    def __init__(self, spacySentence, student):
        self.student = student
        self.words = []

        self.modelTokens = []
        self.modelTokenIds = []
        self.attentionMask = []

        self.actualTokens = []
        self.predictedTokens = []
        self.maskedIndices = []

        self.numMasked = 0
        self.numMaskedPredicted = 0
        self.processSentence(spacySentence)

    """Processes spacy sentence into word objects and creates arrays needed for predicting"""
    def processSentence(self, spacySentence):
        self.modelTokens = [self.student.startToken]
        for sw in spacySentence:
            word = Word(sw, self.student)
            self.words.append(word)
            self.modelTokens.extend(word.modelTokens)
            self.actualTokens.extend(word.actualTokens)
            if word.isMasked:
                self.numMasked += 1

        self.modelTokens.append(self.student.endToken)
        i = 0
        for tok in self.modelTokens:
            if tok == self.student.maskingToken:
                self.maskedIndices.append(i)
            i += 1

        if len(self.modelTokens) > Sentence.staticSentenceMaxTokens:
            raise Exception('Token length should not exceed {}. Token length was: {}'.format(
                Sentence.staticSentenceMaxTokens, len(self.modelTokens)))

        paddingAmount = Sentence.staticSentenceMaxTokens - len(self.modelTokens)
        self.attentionMask.extend([1] * len(self.modelTokens))
        self.modelTokens.extend([self.student.paddingToken] * paddingAmount)
        self.attentionMask.extend([0] * paddingAmount)

        self.modelTokenIds = self.student.tokensToIds(self.modelTokens)


    """Puts a single prediction into the sentence"""
    def updatePrediction(self, predictedIndices):
        predictedTokens = self.student.idsToTokens(predictedIndices)
        self.predictedTokens.append(predictedTokens)

    """Processes all predictions"""
    def updatePredictions(self):
        predictionIndex = 0
        # get the prediction
        for word in self.words:
            if word.isMasked:
                lengthOfWord = word.tokenCount
                word.updatePredictedTokens(self.predictedTokens[predictionIndex: (predictionIndex + lengthOfWord)])
                predictionIndex += lengthOfWord

        # Discover if the word was predicted
        self.numMasked = len(self.maskedIndices)
        for word in self.words:
            if word.isMasked and word.predicted:
                self.numMaskedPredicted += 1

    """Updates the sentence to unmask all words that have been predicted"""
    def unmask(self):
        self.modelTokens = []
        self.attentionMask = []
        self.maskedIndices = []

        for word in self.words:
            self.modelTokens.extend(word.modelTokens)
            if word.isMasked:
                self.numMasked += 1

        i = 0

        for tok in self.modelTokens:
            if tok == self.student.maskingToken:
                self.maskedIndices.append(i)
            i += 1

        paddingAmount = Sentence.staticSentenceMaxTokens - len(self.modelTokens)
        self.attentionMask.extend([1] * len(self.modelTokens))
        self.modelTokens.extend([self.student.paddingToken] * paddingAmount)
        self.attentionMask.extend([0] * paddingAmount)

        self.modelTokenIds = self.student.tokensToIds(self.modelTokens)