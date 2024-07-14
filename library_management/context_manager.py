import json
from contextlib import contextmanager
from .library import Library
from .book_model import BookModel
from .book import Book

@contextmanager
def file_manager(file_name: str, mode: str):
    file = open(file_name, mode)
    try:
        yield file
    finally:
        file.close()

def save_books_to_file(library: Library, file_name: str):
    with file_manager(file_name, 'w') as file:
        books_data = [book._book_model.dict() for book in library._books]
        json.dump(books_data, file)

def load_books_from_file(library: Library, file_name: str):
    with file_manager(file_name, 'r') as file:
        books_data = json.load(file)
        for book_data in books_data:
            book_model = BookModel(**book_data)
            library.add_book(Book(book_model))
