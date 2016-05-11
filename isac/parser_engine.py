from isac.utils.graph.expander import BronKerboschExpander


class Parser(object):

    def __init__(self, tokenizer, tagger):
        self.tokenizer = tokenizer
        self.tagger = tagger

    def score_clique(clique):

        score = 0.0
        for entity in clique:

            _ent = entity.get(
                'entities', [{'confidence': 0.0}])[0].get('confidence')
            score += _ent * len(
                entity.get('entities',
                           [{'match': ''}])[0].get('match')) \
                / (len(utterance) + 1)

        return score

    def parse(self, utterance, N=1):

        tagged = self.tagger.tag(utterance.lower())
        bke = BronKerboschExpander(self.tokenizer)

        parse_results = bke.expand(tagged, scoring_func=self.score_clique)
        count = 0

        for result in parse_results:
            count += 1
            parse_confidence = 0.0

            for tag in result:
                sample_entity = tag['entities'][0]
                entity_confidence = sample_entity.get('confidence', 0.0) \
                    * float(len(sample_entity.get('match'))) / len(utterance)
                parse_confidence += entity_confidence

            yield {
                'utterance': utterance,
                'tags': result,
                'confidence': parse_confidence
            }

            if count >= N:
                break
