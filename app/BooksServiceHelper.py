searchQueryNames = {'author': 'inauthor', 'title': 'intitle'}


class RequestHelper:
    def __init__(self):
        self.__list_params = {}
        self.__field_root = None

    def query(self, query):
        self.__list_params['q'] = query

    def __str__(self):
        result = ''
        for key, value in self.__list_params.items():
            result += key
            result += ': '
            result += str(value)
            result += ' '
        return result

    def max_results(self, value):
        self.__list_params['maxResults'] = value

    def get(self, key):
        return self.__list_params[key]
