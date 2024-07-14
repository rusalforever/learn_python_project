from .book_model import BookModel

class Book:
    def __init__(self, book_model: BookModel):
        self._book_model = book_model

    def get_ribbon(self) -> str:
        return f"{self._book_model.title} by {self._book_model.author}, published in {self._book_model.year_of_publication}"
