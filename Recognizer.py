import json

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as FR_STOP
from textacy import extract
from difflib import SequenceMatcher

nlp = spacy.load("fr_core_news_sm")


class Recognize:

    def __init__(self, dic: dict):
        self.words_dic = dic
        self.similarity_value = 0.8

    @staticmethod
    def knowledge_factory(knowledge):
        instance = Recognize(knowledge.get_optimized_dic())

        return instance

    @staticmethod
    def main_tokens(text: str):
        i = 0
        tokens = []
        doc = nlp(text)
        for token in doc:
            if token.text not in FR_STOP and token.pos_ != "PUNCT" and token.pos_ != "PRON":
                tokens.append([i, str(token.lemma_), token.pos_])
                i = i + 1
        return tokens

    @staticmethod
    def bigrams(text: str):
        doc = nlp(text)
        return list(extract.basics.ngrams(doc, 2))

    @staticmethod
    def trigrams(text: str):
        doc = nlp(text)
        return list(extract.basics.ngrams(doc, 3))

    @staticmethod
    def similar(a: str, b: str):
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def get_lemma(text):
        text = text.lower()
        doc = nlp(text)

        result = ""
        for token in doc:
            result += str(token.lemma_) + " "
        return result[:-1]

    def search_similar(self, text: str):
        # print(text,similar(text,"france"))
        similarities = [Recognize.similar(text, key) for key in self.words_dic.keys()]
        index = similarities.index(max(similarities))
        # print(text_lemma,list(data.values())[index],similarities[index])
        if similarities[index] > self.similarity_value:
            return list(self.words_dic.values())[index], similarities[index]
        return None

    def search(self, text: str):
        key = Recognize.get_lemma(text)
        if key in self.words_dic.keys():
            return self.words_dic[Recognize.get_lemma(text)]
        else:
            return None

    def ner_text(self, text):
        dic = {}
        trigram = Recognize.trigrams(text)
        for token in trigram:
            result = self.search(Recognize.get_lemma(str(token)))
            if result is not None:
                text = text.replace(str(token), '')

                if dic.get(result[0]) is None:
                    dic[result[0]] = []

                dic[result[0]].append({"value": result[1], "confidence": 1})

        bigram = Recognize.bigrams(text)
        for token in bigram:
            result = self.search(Recognize.get_lemma(str(token)))
            if result is not None:
                text = text.replace(str(token), '')
                if dic.get(result[0]) is None:
                    dic[result[0]] = []

                dic[result[0]].append({"value": result[1], "confidence": 1})

        tokens = Recognize.main_tokens(text)
        for token in tokens:
            result = self.search(token[1])
            if result is not None and result[0] in ['quantite', 'prix', 'caliber', 'conditionnement'] and \
                    tokens[token[0] - 1][2] == "NUM":
                if dic.get(result[0]) is None:
                    dic[result[0]] = []

                dic[result[0]].append({"value": tokens[token[0] - 1][1] + result[1], "confidence": 1})

            elif result is not None:
                if dic.get(result[0]) is None:
                    dic[result[0]] = []

                dic[result[0]].append({"value": result[1], "confidence": 1})

            elif self.similarity_value < 1:
                result = self.search_similar(self.get_lemma(token[1]))
                if result is not None:
                    if dic.get(result[0][0]) is None:
                        dic[result[0][0]] = []

                    dic[result[0][0]].append({"value": result[0][1], "confidence": result[1]})

        return dic

    def ner_text_json(self, text):
        result = self.ner_text(text)
        return json.dumps(result)
