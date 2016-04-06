from app.FieldNode import *

searchQueryNames = {'author': 'inauthor', 'title': 'intitle'}


class RequestHelper:
    def __init__(self):
        self.q = None
        self.fields = FieldTree("items")
        self.maxResults = 0

    def query(self, query):
        assert isinstance(query, str)
        self.q = query

    def max_results(self, max_results):
        self.maxResults = max_results

    def add_item(self, parent, field):
        self.fields.add_child(parent, field)

    def add_items(self, parent, *args):
        for arg in args:
            assert isinstance(arg, str)
            self.add_item(parent, arg)