from app.models import Term
from app.constants import Provider


class ParametersParser:
    def __init__(self, parameters):
        self.parameters = parameters

    def parse_parameters(self):
        formatted_params = {}
        for provider in Provider.get_list():
            formatted_params[provider] = {}
            for key, val in self.parameters.items():
                if key == 'categories' and val is not None:
                    value = self._find_matched_categories(val.split(','), provider)
                else:
                    value = val
                formatted_key = Term.query.filter_by(term=key, provider=provider).first().matched_term
                formatted_params[provider][formatted_key] = value

        return formatted_params

    def _find_matched_categories(self, categories, provider):
        matched_categories = set()
        for category in categories:
            term = Term.query.filter_by(term=category, provider=provider).first().matched_term
            matched_categories.add(term)
        return matched_categories
