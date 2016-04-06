import unittest
from app import FieldNode
from app.FieldNode import FieldTree
from app.BookManager import BookManager
from app.BooksServiceHelper import RequestHelper


class TestCase(unittest.TestCase, ):
    def setUp(self):
        self.field_tree = FieldTree("items")

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

    def test_book_manager(self):
        bm = BookManager()
        rh = RequestHelper()
        rh.query("carrie+inauthor:king")
        rh.add_item("items", "volumeInfo")
        rh.add_items("volumeInfo", "authors", "description", "categories")
        rh.max_results(2)
        result = bm.search(rh)
        assert len(result) > 0


if __name__ == '__main__':
    unittest.main()