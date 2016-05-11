from isac.utils.common.intent_helpers import find_first_tag, resolve_one_of


class Intent(object):

    def __init__(self, name, requires, at_least_one, optional):
        self.name = name
        self.requires = requires
        self.at_least_one = at_least_one
        self.optional = optional

    def validate(self, tags, confidence):

        result = {'intent_type': self.name}
        intent_confidence = 0.0
        local_tags = tags[:]

        for require_type, attr_name in self.requires:
            required_tag, canonical_form = find_first_tag(
                local_tags, require_type)

            if not required_tag:
                result['confidence'] = 0.0
                return result

            result[attr_name] = canonical_form
            local_tags.remove(required_tag)
            intent_confidence += 1.0

        for optional_type, attr_name in self.optional:
            optional_tag, canonical_form = find_first_tag(
                local_tags, optional_type)

            if not optional_tag or attr_name in result:
                continue

            result[attr_name] = canonical_form
            local_tags.remove(optional_tag)
            intent_confidence += 1.0

        total_confidence = intent_confidence / len(tags) * confidence

        target_client, canonical_form = find_first_tag(local_tags, 'Client')

        result['confidence'] = total_confidence

        return result


class IntentBuilder(object):

    def __init__(self, name):
        self.at_least_one = []
        self.requires = []
        self.optional = []
        self.name = name

    def one_of(self, *args):

        self.at_least_one.append(args)
        return self

    def require(self, e_type, attr_name=None):

        if not attr_name:
            attr_name = e_type
        self.requires += [(e_type, attr_name)]
        return self

    def optionally(self, e_type, attr_name=None):

        if not attr_name:
            attr_name = e_type
        self.optional += [(e_type, attr_name)]
        return self

    def build(self):

        return Intent(
            self.name, self.requires, self.at_least_one, self.optional)
