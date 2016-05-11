
class TrieNode(object):

    def __init__(self, data=None, is_terminal=False):
        self.data = set()
        self.is_terminal = is_terminal
        self.children = {}
        self.key = None
        if data:
            self.data.add(data)

    def lookup(self, iterable, index=0, gather=False, edit_distance=0,
               max_edit_distance=0, match_threshold=0.0, matched_length=0):

        if self.is_terminal:
            if index == len(iterable) or (gather and index < len(iterable) \
                    and iterable[index] == ' '):
                _key_conf = float(len(self.key) - edit_distance)
                _key_max = float(max(len(self.key), index))
                confidence = _key_conf / _key_max
                if confidence > match_threshold:
                    yield {
                        'key': self.key,
                        'match': iterable[:index],
                        'data': self.data,
                        'confidence': confidence
                    }

        if index < len(iterable) and iterable[index] in self.children:
            for result in self.children[iterable[index]]\
                    .lookup(iterable, index + 1, gather=gather,
                            edit_distance=edit_distance,
                            max_edit_distance=max_edit_distance,
                            matched_length=matched_length + 1):
                yield result

        _dist_conf = float(
            index - edit_distance + (max_edit_distance - edit_distance))
        _dist_opt_conf = (float(index) + (max_edit_distance - edit_distance))
        _pc = _dist_conf / _dist_opt_conf \
            if index + max_edit_distance - edit_distance > 0 else 0.0

        if edit_distance < max_edit_distance and _pc > match_threshold:
            for child in list(self.children):
                if index >= len(iterable) or child != iterable[index]:
                    for result in self.children[child]\
                        .lookup(iterable, index + 1, gather=gather,
                                edit_distance=edit_distance + 1,
                                max_edit_distance=max_edit_distance,
                                matched_length=matched_length):
                        yield result
                    for result in self.children[child]\
                        .lookup(iterable, index + 2, gather=gather,
                                edit_distance=edit_distance + 1,
                                max_edit_distance=max_edit_distance,
                                matched_length=matched_length):
                        yield result
                    for result in self.children[child]\
                        .lookup(iterable, index, gather=gather,
                                edit_distance=edit_distance + 1,
                                max_edit_distance=max_edit_distance,
                                matched_length=matched_length):
                        yield result

    def insert(self, iterable, index=0, data=None, value=None):

        if index == len(iterable):
            self.is_terminal = True
            self.key = iterable
            if data:
                self.data.add(data)
        else:
            if iterable[index] not in self.children:
                self.children[iterable[index]] = TrieNode()
            self.children[iterable[index]].insert(iterable, index + 1, data)

    def is_prefix(self, iterable, index=0):

        if iterable[index] in self.children:
            return self.children[iterable[index]].is_prefix(
                iterable, index + 1)
        else:
            return False

    def remove(self, iterable, data=None, index=0):

        if index == len(iterable):
            if self.is_terminal:
                if data:
                    self.data.remove(data)
                    if len(self.data) == 0:
                        self.is_terminal = False
                else:
                    self.data.clear()
                    self.is_terminal = False
                return True
            else:
                return False
        elif iterable[index] in self.children:
            return self.children[iterable[index]].remove(
                iterable, index=index+1, data=data)
        else:
            return False


class Trie(object):

    def __init__(self, max_edit_distance=0, match_threshold=0.0):
        self.root = TrieNode('root')
        self.max_edit_distance = max_edit_distance
        self.match_threshold = match_threshold

    def gather(self, iterable):

        for result in self.lookup(iterable, gather=True):
            yield result

    def lookup(self, iterable, gather=False):

        for result in self.root.lookup(iterable,
                                       gather=gather,
                                       edit_distance=0,
                                       max_edit_distance=self.max_edit_distance,
                                       match_threshold=self.match_threshold):
            yield result

    def insert(self, iterable, data=None):

        self.root.insert(iterable, index=0, data=data)

    def remove(self, iterable, data=None):

        return self.root.remove(iterable, data=data)
