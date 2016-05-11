from isac.intent_engine import IntentBuilder


class Trainer(object):

    def __init__(self, engine):
        self.training_data = engine.training_data
        self.engine = engine
        self.tokenizer = engine.tokenizer
        self.tagger = engine.tagger

    def register_entities(self, intent):

        for _data in intent['training']:
            for entity in _data.get('tags'):
                self.engine.register_entity(entity['value'], entity['key'])

    def pos_training_data(self):

        for intent in self.training_data:
            for _t in intent['training']:
                for tag in _t['tags']:
                    for pos in self.tokenizer.tagger(_t['text']):
                        if pos[0] == tag['value']:
                            tag['pos'] = pos[1]

    def build(self):

        self.pos_training_data()
        for intent in self.training_data:
            self.register_entities(intent)
            self.engine.register_intent(
                intent['name'], intent['required'], intent['optional'])
