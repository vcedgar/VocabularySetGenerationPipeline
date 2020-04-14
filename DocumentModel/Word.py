class Word:
    """ A class used to represent a single word in a document.

        Attributes:
            text: the original text of the word.
            lemma: the text of the lemma the word belongs to.
            isMasked: whether this word is known by the user.
            tokens: the original tokens that make up the word.
            modelTokens: tokens used my the model (either the masked token or the original.
            predictedTokenLists: the lists of tokens that the model predicted for each token
            correctPredictionCount: number of tokens that were correctly predicted
            tokenCount: the total number of tokens
    """
    # have the Word class store synonyms
    def __init__(self, spacyWord, student):
        self.text = spacyWord.text
        self.lemma = spacyWord.lemma_
        self.actualTokens = student.getSubWordTokens(self.text)
        self.tokenCount = len(self.actualTokens)
        self.modelTokens = self.actualTokens
        self.predicted = True
        self.student = student

        self.isMasked = not student.isSpacyWordKnown(spacyWord)
        if self.isMasked:
            self.modelTokens = [student.maskingToken] * self.tokenCount
            self.predicted = False

    def updatePredictedTokens(self, bertResponse):
        self.predicted = self.student.isWordPredicted(bertResponse, self.lemma)

        # numberOfGuess = self.student.guesses
        # correctCount = 0
        # if (self.isMasked):
        #     for i in range(numberOfGuess):
        #         for j in range(len(self.actualTokens)):
        #             if self.actualTokens[j] == bertResponse[j][i]:
        #                     correctCount += 1
        #     # happens with newlines sometimes
        #     if self.tokenCount == 0:
        #         self.correctPredictionPercent = 1
        #     else:
        #         self.correctPredictionPercent = correctCount / self.tokenCount

    """If the word has been predicted this will unmask it"""
    def unmask(self):
        self.isMasked = False
        self.modelTokens = self.actualTokens
