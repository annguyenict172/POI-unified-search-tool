import nltk


def extract_arguments(query_text):
    location, name, nouns = _extract_potential_keywords(query_text)
    return {
        'location': location,
        'name': name,
        'types': nouns
    }


def _extract_potential_keywords(text):
    nouns = []
    name = ''
    location = ''

    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    for w in tagged:
        if w[1] == 'NN':
            nouns.append(w[0])

    for chunk in nltk.ne_chunk(tagged):
        if hasattr(chunk, 'label'):
            if chunk.label() == 'PERSON':
                name = ' '.join(c[0] for c in chunk)
            if chunk.label() == 'GPE':
                location = ' '.join(c[0] for c in chunk)

    return location, name, nouns
