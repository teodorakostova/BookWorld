from apiclient import discovery
from apiclient.discovery import build
from googleconf import DEVELOPERS_CODE

class BookManager:
    class ServiceBuilder:
        def __init__(self, service_name, version, developer_key):
            self.service_name = service_name
            self.version = version
            self.developer_key = developer_key

        def build_service(self):
            return build(self.service_name, self.version, developerKey=self.developer_key)

    def __init__(self):
        service_builder = self.ServiceBuilder('books', 'v1', DEVELOPERS_CODE)
        self.service = service_builder.build_service()

    def search(self, requestHelper):
        return self.service.volumes().list(**requestHelper.__dict__).execute()