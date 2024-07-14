from .book import Book
from .book_model import BookModel

class Journal(Book):
    def __init__(self, book_model: BookModel, issue_number: int):
        super().__init__(book_model)
        self._issue_number = issue_number

    def get_ribbon(self) -> str:
        return f"{self._book_model.title} by {self._book_model.author}, published in {self._book_model.year_of_publication}, Issue: {self._issue_number}"
