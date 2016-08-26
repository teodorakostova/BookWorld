import unittest
from app import FieldNode
from app.FieldNode import FieldTree
from app.BookManager import BookManager
from app.BooksServiceHelper import RequestHelper


class TestCase(unittest.TestCase, ):
    def setUp(self):
        self.field_tree = FieldTree("items")
        self.bm = BookManager()
        self.rh = RequestHelper()

    def test_add_two_children(self):
        self.field_tree.add_child("items", "volumeInfo")
        self.field_tree.add_child("volumeInfo", "author")
        assert "items(volumeInfo(author))" == str(self.field_tree)

    def test_add_more_children(self):
        self.field_tree.add_child("items", "volumeInfo")
        self.field_tree.add_child("volumeInfo", "authors")
        self.field_tree.add_child("volumeInfo", "categories")
        self.field_tree.add_child("volumeInfo", "description")
        self.field_tree.add_child("volumeInfo", "mainCategory")
        assert str(self.field_tree) == "items(volumeInfo(authors, categories, description, mainCategory))"

    def test_bm_simple_query(self):
        self.rh.query("Way station")
        self.rh.add_item(None, "volumeInfo")
        self.rh.add_items("volumeInfo", "authors", "categories", "imageLinks")
        self.rh.max_results(2)
        result = self.bm.search(self.rh)
        print("SIMPLE QUERY RESULT")
        print(result)
        assert len(result) > 0

    def test_book_manager(self):
        self.rh.query("carrie+inauthor:king")
        self.rh.add_item("items", "volumeInfo")
        self.rh.add_items("volumeInfo", "authors", "description", "categories")
        self.rh.max_results(2)
        result = self.bm.search(self.rh)
        print(result)
        assert len(result) > 0

    def test_get_info(self):
        test_result = {'items': [
            {'volumeInfo': {'categories': ['Fiction'], 'authors': ['Clifford D. Simak']}},
            {'volumeInfo': {'categories': ['Fiction'], 'authors': ['Paul Lederer']}}]}

        for item in test_result['items']:
            for k, v in item['volumeInfo'].items():
                print(k, " :", v[0])

        assert 1 == 1


if __name__ == '__main__':
    unittest.main()
