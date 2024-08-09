from typing import List, Generator
from .models import Book
from .decorators import book_added_log, book_exists


class Library:
    def __init__(self, books: List[Book]):
        self._books = books

    @property
    def books(self) -> List[Book]:
        return self._books

    def __iter__(self):
        return iter(self._books)

    def books_by_author(self, author: str) -> Generator[Book, None, None]:
        return (book for book in self._books if book.author == author)

    @book_added_log
    def add(self, book: Book):
        self._books.append(book)

    @book_exists
    def remove(self, book: Book):
        self._books.remove(book)


