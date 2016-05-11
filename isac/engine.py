import re
import heapq

from isac.entity_engine import Entity
from isac.intent_engine import IntentBuilder
from isac.parser_engine import Parser
from isac.utils.nlp.tokenizer import Tokenizer
from isac.utils.nlp.trie import Trie


class Engine(object):

    def __init__(self, tokenizer=None, trie=None):
        self.tokenizer = tokenizer or Tokenizer()
        self.trie = trie or Trie()
        self.tagger = Entity(self.trie, self.tokenizer)
        self.nn_training = []
        self.intent_parsers = []

    def _max_intent(self, parse_result):

        max_intent = None
        for intent in self.intent_parsers:
            i = intent.validate(
                parse_result.get('tags'), parse_result.get('confidence'))
            if not max_intent or (
                    i and i.get('confidence') > max_intent.get('confidence')):
                max_intent = i

        return max_intent

    def calculate_intent(self, utterance, results=1):

        parser = Parser(self.tokenizer, self.tagger)

        for result in parser.parse(utterance, N=results):
            max_intent = self._max_intent(result)

        if max_intent and max_intent.get('confidence', 0.0) > 0:
            yield max_intent

    def register_entity(self, value, entity_type, alias_of=None):

        if alias_of:
            self.trie.insert(value, data=(alias_of, entity_type))
        else:
            self.trie.insert(value.lower(), data=(value, entity_type))
            self.trie.insert(entity_type.lower(),
                             data=(entity_type, 'Node'))

    def training_nouns(self, value, entity_type):

        if self.tokenizer.np_chunker(value):

            if entity_type not in self.nn_training:
                self.nn_training.append(entity_type)

    def pos_training(self, training):

        for tag in training['tags']:

            for pos in self.tokenizer.tagger(training['text']):
                if pos[0] == tag['value']:
                    tag['pos'] = pos[1]

        return training

    def register_training(self, data):

        for tag in data.get('tags'):
            self.register_entity(tag['value'], tag['key'])

    def register_intent_parser(self, intent_parser):

        if hasattr(intent_parser, 'validate') and \
                callable(intent_parser.validate):
            self.intent_parsers.append(intent_parser)
        else:
            raise ValueError('Invalid intent parser')

    def register_intent(self, name, required, optional=None):

        _i = IntentBuilder(name)

        for _r in required:
            _i.require(_r)

        if optional:
            for _o in optional:
                _i.optional(_o)

        _i = _i.build()
        self.register_intent_parser(_i)
