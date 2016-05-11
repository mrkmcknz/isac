from textblob import TextBlob
from textblob.np_extractors import ConllExtractor


class Tokenizer(object):

    def __init__(self):
        pass

    def tokenize(self, text):

        text = TextBlob(text)
        return text.words

    def np_chunker(self, text):

        extractor = ConllExtractor()
        text = TextBlob(text, np_extractor=extractor)
        return text.noun_phrases

    def tagger(self, text):

        text = TextBlob(text)
        return text.tags
