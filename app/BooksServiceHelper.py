searchQueryNames = {'author': 'inauthor', 'title': 'intitle'}


# class BooksSearchQuery:


class BookVolumesManager:
    def __init__(self):
        pass

    def add_query_params(self, query):
        if self.__baseURL[-1] != '?':
            self.__baseURL += '?'
        for key, value in query.items():
            self.__baseURL += key
            self.__baseURL += '='
            self.__baseURL += value
            self.__baseURL += '&'


class FieldNode:
    def __init__(self, name, subresources=None):
        self.__name = name
        self.__repr = self.__name
        if subresources is None:
            self.__subresources = []
        else:
            self.__subresources = subresources

    def __str__(self):
        self.__repr = self.__name
        if len(self.__subresources) > 0:
            self.__repr += '('
            for i, resource in enumerate(self.__subresources):
                self.__repr += str(resource)
                if i != len(self.__subresources) - 1:
                    self.__repr += ','
            self.__repr += ')'
        return self.__repr

    def subresource(self, subresource):
        self.__subresources.append(subresource)

    def add_subresources(self, *args):
        for resource in args:
            self.__subresources.append(resource)

    def add_sibling(self, sibling):
        self.__repr += ','
        self.__repr += str(sibling)


# google books api element representations
class VolumeInfo:
    def __init__(self, title, authors, description, avrgRating):
        self.__title = title
        self.__authors = authors
        self.__desciption = description
        self.__avrgRating = avrgRating


class VolumeItem:
    def __init__(self, id, volumeInfo):
        self.__id = id
        self.__volumeInfo = volumeInfo


def test_create_url():
    fields = 'fields'
    items = FieldNode('items')
    volumeInfo = FieldNode('volumeInfo')
    title = FieldNode('title')
    authors = FieldNode('authors')
    description = FieldNode('description')
    volumeInfo.add_subresources(title, authors, description)
    items.subresource(volumeInfo)
    print(items)


def test_make_request():
    pass


if __name__ == '__main__':
    test_create_url()
