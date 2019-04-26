import nltk


def extract_nouns_and_location(text):
    nouns = []
    location = ''

    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    for w in tagged:
        if w[1] == 'NN':
            nouns.append(w[0])

    for chunk in nltk.ne_chunk(tagged):
        if hasattr(chunk, 'label'):
            if chunk.label() == 'GPE':
                location = ' '.join(c[0] for c in chunk)

    return nouns, location
