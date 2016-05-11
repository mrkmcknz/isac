
def find_first_tag(tags, entity_type, after_index=-1):

    for tag in tags:
        for entity in tag.get('entities'):
            for v, t in entity.get('data'):
                if t.lower() == entity_type.lower() and \
                        tag.get('start_token') > after_index:
                    return tag, v

    return None, None


def choose_1_from_each(lists):

    if len(lists) == 0:
        yield []

    else:
        for el in lists[0]:
            for next_list in choose_1_from_each(lists[1:]):
                yield [el] + next_list


def resolve_one_of(tags, at_least_one):

    if len(tags) < len(at_least_one):
        return None

    for possible_resolution in choose_1_from_each(at_least_one):
        resolution = {}
        pr = possible_resolution[:]

        for entity_type in pr:
            last_end_index = 0

            if entity_type in resolution:
                last_end_index = resolution.get[entity_type][-1]\
                    .get('end_token')
            tag, value = find_first_tag(
                tags, entity_type, after_index=last_end_index)

            if not tag:
                break

            else:
                if entity_type not in resolution:
                    resolution[entity_type] = []
                resolution[entity_type].append(tag)

        if len(resolution) == len(possible_resolution):
            return resolution

    return None
