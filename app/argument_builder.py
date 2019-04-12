import nltk


class ArgumentBuilder:
    args = {
        'location': '',
        'name': '',
        'types': []
    }

    def build_api_arguments(self, query_text):
        self._extract_potential_keywords(query_text)
        return self.args

    def _extract_potential_keywords(self, text):
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        for w in tagged:
            if w[1] == 'NN':
                self.args['types'].append(w[0])

        for chunk in nltk.ne_chunk(tagged):
            if hasattr(chunk, 'label'):
                if chunk.label() == 'PERSON':
                    self.args['name'] = ' '.join(c[0] for c in chunk)
                if chunk.label() == 'GPE':
                    self.args['location'] = ' '.join(c[0] for c in chunk)
