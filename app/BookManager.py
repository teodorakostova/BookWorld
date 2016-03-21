import requests
from apiclient import discovery
from apiclient.discovery import build
from .googleconf import DEVELOPERS_KEY
from .BooksServiceHelper import FieldNode


# res = service.volumes().list(q='carrie+inauthor:king',
#                            fields='items(volumeInfo(authors,categories,description,mainCategory,publishedDate,publisher,title))',
#                           maxResults=3).execute()


class ServiceBuilder:
    def __init__(self, service_name, version, developer_key):
        self.__service_name = service_name
        self.__version = version
        self.__developer_key = developer_key

    def build_service(self):
        return build(self.__service_name, self.__version, self.__developer_key)


class RequestHelper:
    def __init__(self):
        self.__list_params = {}

    def field(self, field):
        fields_param = self.__list_params.get('fields')
        new_field = FieldNode(field)
        if fields_param is not None:
            self.__list_params['fields'] = fields_param.add_sibling(field)
        else:
            self.__list_params['fields'] = new_field

    def subfield(self, parent, resource):
        pass

    def max_results(self, value):
        self.__list_params['maxResults'] = value


class BookManager:
    def __init__(self):
        serviceBuilder = ServiceBuilder('books', 'v1', DEVELOPERS_KEY)
        self.__service = serviceBuilder.build_service()

    def search(self, query, fields, **kwargs):
        self.__service.volumes().list(q=query, fields=fields, **kwargs).execute()


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


if __name__ == '__main__':
    bm = BookManager()
    rh = RequestHelper()
    rh.query('carrie+inauthor:king')
    rh.field('items')
