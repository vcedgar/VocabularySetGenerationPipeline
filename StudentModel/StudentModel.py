import torch
from pytorch_transformers import BertForMaskedLM, BertTokenizer
import spacy

class StudentModel:

    def __init__(self, vocabulary, config):
        spacy.prefer_gpu()
        self.spacyNlp = spacy.load("en_core_web_lg")
        self.simThreshold = 0.70

        self.modelName = config["bertModel"]
        self.guesses = config["numberOfGuesses"]
        self.useSimilarity = config["useSimilarity"]
        self.useSynonyms = config["useSynonyms"]

        self.bertModel = BertForMaskedLM.from_pretrained(self.modelName).cuda()
        self.bertTokenizer = BertTokenizer.from_pretrained(self.modelName)
        self.maskingToken = "[MASK]"
        self.paddingToken = "[PAD]"
        self.startToken = "[CLS]"
        self.endToken = "[SEP]"

        self.vocabulary = vocabulary

    def predict(self, sentence):
        # print(self.idsToTokens(sentence.modelTokenIds))
        tensors = torch.tensor(sentence.modelTokenIds).cuda().unsqueeze(0).cuda()
        attentionMaskTensors = torch.tensor(sentence.attentionMask).cuda().unsqueeze(0).cuda()

        self.bertModel.eval().cuda()
        # print(tensors, attentionMaskTensors)
        with torch.no_grad():
            outputs = self.bertModel(tensors, attentionMaskTensors)
            predictions = outputs[0][0]

        for index in sentence.maskedIndices:
            values, predictedIndices = torch.topk(predictions[index], self.guesses)
            sentence.updatePrediction(predictedIndices.tolist())
        sentence.updatePredictions()

    def isSpacyWordKnown(self, word):
        """If a word is in the known vocabulary list, or it is a named entity, or it is not actually a word it is
        known."""
        entity = (word.ent_iob != 0 and word.ent_iob != 2)
        correctType = self.isSpacyWordCorrectType(word)
        if entity or (not correctType) or (not word.is_alpha) or (word.lemma_ in self.vocabulary):
            return True
        return False

    def isSpacyWordCorrectType(self, word):
        isNoun = word.pos_ == "NOUN"
        isAdj = word.pos_ == "ADJ"
        isAdv = word.pos_ == "ADV"
        isVerb = word.pos_ == "VERB"
        return isNoun or isAdj or isAdv or isVerb

    def tokensToIds(self, tokens):
        return self.bertTokenizer.convert_tokens_to_ids(tokens)

    def idsToTokens(self, ids):
        return self.bertTokenizer.convert_ids_to_tokens(ids)

    def getSubWordTokens(self, wordText):
        return self.bertTokenizer.wordpiece_tokenizer.tokenize(wordText)

    def isWordPredicted(self, bertResponse, realAnswerLemma):
        if len(bertResponse) != 1:
            singleTokenList = []
            for i in range(self.guesses):
                finalTokens = []
                for tokenList in bertResponse:
                    token = tokenList[i]
                    t = token.replace("#", "")
                    finalTokens.append(t)
                prediction = ""
                prediction = prediction.join(finalTokens)
                singleTokenList.append(prediction)
            bertResponse = []
            bertResponse.extend(singleTokenList)
        else:
            bertResponse = bertResponse[0]
        return self.parseSingleTokenBERT(bertResponse, realAnswerLemma)

    def parseSingleTokenBERT(self, bertResponse, answer):
        isExactLemma, itIsSynonym, itIsSimilar = False, False, False
        for i in range(self.guesses):
            resp = bertResponse[i]
            if resp == answer or self.isLemma(answer, resp):
                isExactLemma = True
            try:
                if self.useSynonyms:
                    itIsSynonym = self.isSynonym(answer, resp)
            except:
                print("err")
            try:
                if self.useSimilarity:
                    itIsSimilar = self.isSimilar(answer, resp)
            except:
                print("err")

        return isExactLemma or itIsSimilar or itIsSynonym

    def isLemma(self, lemma, target):
        doc = self.spacyNlp(target)
        targSpan = doc[0]
        targLemma = targSpan.lemma_
        return lemma == targLemma

    def isSimilar(self, word, target):

        tokens = word + " * " + target
        doc = self.spacyNlp(tokens)
        index = 0
        for tok in doc:
            if tok.text == "*":
                break
            index += 1
        wordSpan = doc[0:index]
        targSpan = doc[(index + 1):]
        similarity = wordSpan.similarity(targSpan)
        return similarity > self.simThreshold

    def isSynonym(self, word, target):
        pass
        # Would be used if it weren't for the API licence
        # url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word \
        #       + KEY
        # try:
        #     resp = requests.get(url=url)
        #     j = resp.json()
        #     for wordObj in j:
        #             if "meta" in wordObj and "syns" in wordObj["meta"]:
        #                 synList = wordObj["meta"]["syns"]
        #                 for synonyms in synList:
        #                     if target in synonyms:
        #                         return True
        # except Exception:
        #     print("Target word: " + word + " threw exception while searching for synonyms")
        # return False