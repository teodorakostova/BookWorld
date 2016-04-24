from app.FieldNode import *

searchQueryNames = {'author': 'inauthor', 'title': 'intitle'}


class RequestHelper:
    def __init__(self):
        self.q = None
        self.fields = None
        self.maxResults = 1

    def query(self, query):
        assert isinstance(query, str)
        self.q = query

    def max_results(self, max_results):
        self.maxResults = max_results

    def add_item(self, parent, field):
        if self.fields is None:
            self.fields = FieldTree("items")
        if parent is None:
            parent = "items"
        self.fields.add_child(parent, field)

    def add_items(self, parent, *args):
        if self.fields is None:
            self.fields = FieldTree("items")
        for arg in args:
            assert isinstance(arg, str)
            self.add_item(parent, arg)