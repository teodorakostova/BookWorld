from apiclient import discovery
from apiclient.discovery import build
from googleconf import DEVELOPERS_KEY


class ServiceBuilder:
    def __init__(self, service_name, version, developer_key):
        self.__service_name = service_name
        self.__version = version
        self.__developer_key = developer_key

    def build_service(self):
        return build(self.__service_name, self.__version, developerKey=self.__developer_key)


class BookManager:
    def __init__(self):
        serviceBuilder = ServiceBuilder('books', 'v1', DEVELOPERS_KEY)
        self.__service = serviceBuilder.build_service()

    def search_inner(self, query, fields, **kwargs):
        return self.__service.volumes().list(q=query, fields=fields, **kwargs).execute()

    def search(self, requestHelper):
        return self.search_inner(requestHelper.get('q'), requestHelper.get('fields'))
