from fuzzywuzzy import fuzz


def snake_case_to_lower_words(snake_string):
    components = snake_string.split('_')
    return ' '.join(x for x in components)


def get_similar_ratio(string1, string2):
    return fuzz.ratio(string1, string2)
