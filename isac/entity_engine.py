from six.moves import xrange

from isac.utils.nlp.trie import Trie
from isac.utils.common.helpers import most_common


class Entity(object):

    def __init__(self, trie, tokenizer, training, max_tokens=20):
        self.trie = trie
        self.training = training
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def _iterate_subsequences(self, tokens):

        for start_x in xrange(len(tokens)):
            for end_x in xrange(start_x + 1, len(tokens) + 1):
                yield ' '.join(tokens[start_x:end_x]), start_x

    def _sort_and_merge_tags(self, tags):

        decorated = [(
            tag['start_token'], tag['end_token'], tag) for tag in tags]
        decorated.sort()
        return [tag for start_token, end_token, tag in decorated]

    def unknown_entities(self, attr, utterance):

        pos_tokens = []
        for _t in self.training:
            pos_tokens += [t['pos'] for t in _t['tags'] if t['key'] == attr]

        # Change to RF classifier or something PLEASE
        most_common_pos = most_common(pos_tokens)

        for pos in self.tokenizer.tagger(data['text']):
            if pos[1] == most_common_pos:
                return pos[0]

        return None

    def tag(self, utterance):

        tokens = self.tokenizer.tokenize(utterance)
        entities = []
        additional_sort = len(entities) > 0

        for i in xrange(len(tokens)):
            part = ' '.join(tokens[i:])

            for entity in self.trie.gather(part):
                entity['data'] = list(entity['data'])
                entities.append({
                    'match': entity.get('match'),
                    'key': entity.get('key'),
                    'start_token': i,
                    'entities': [entity],
                    'end_token': i + len(
                        self.tokenizer.tokenize(entity.get('match')))
                })

        if additional_sort:
            entities = self._sort_and_merge_tags(entities)

        return entities
