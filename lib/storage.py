import json
from contextlib import contextmanager
from .library import Library
from .models import Book, BookModel


@contextmanager
def file_manager(file_name: str, mode: str):
    file = open(file_name, mode)
    try:
        yield file
    finally:
        file.close()


def save(library: Library, file_name: str):
    with file_manager(file_name, 'w') as file:
        books_data = [book._model.dict() for book in library]
        json.dump(books_data, file)


def load(library: Library, file_name: str):
    with file_manager(file_name, 'r') as file:
        books_data = json.load(file)
        for book_data in books_data:
            book_model = BookModel(**book_data)
            library.add(Book(book_model))
