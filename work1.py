from pydantic import BaseModel
from typing import List, Optional
import json
import os

class BookModel(BaseModel):
    title: str
    author: str
    year: int

class Book:
    def __init__(self, model: BookModel):
        self._model = model

    def __str__(self):
        return f"{self._model.title} by {self._model.author} ({self._model.year})"
########################################

class Library:
    def __init__(self):
        self._books = []

    def add_book(self, book: Book):
        self._books.append(book)

    def remove_book(self, book: Book):
        self._books.remove(book)

    def __iter__(self):
        return iter(self._books)

    def books_by_author(self, author: str):
        for book in self._books:
            if book._model.author == author:
                yield book

    def __str__(self):
        return "\n".join(str(book) for book in self._books)

from functools import wraps

def log_action(action):
    def decorator(func):
        @wraps(func)
        def wrapper(self, book: Book):
            result = func(self, book)
            print(f"{action} book: {book}")
            return result
        return wrapper
    return decorator

def check_book_exists(func):
    @wraps(func)
    def wrapper(self, book: Book):
        if book in self._books:
            return func(self, book)
        else:
            print(f"Book not found: {book}")
    return wrapper

class LibraryFileManager:
    def __init__(self, filepath: str, library: Library):
        self.filepath = filepath
        self.library = library

    def __enter__(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                books_data = json.load(file)
                for book_data in books_data:
                    book_model = BookModel(**book_data)
                    self.library.add_book(Book(book_model))
        return self.library

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.filepath, 'w') as file:
            books_data = [book._model.dict() for book in self.library]
            json.dump(books_data, file)


class Journal(Book):
    def __init__(self, model: BookModel, issue: int):
        super().__init__(model)
        self.issue = issue

    def __str__(self):
        return f"{self._model.title} by {self._model.author} (Issue {self.issue}, {self._model.year})"

from abc import ABC, abstractmethod

class Printable(ABC):
    @abstractmethod
    def print_details(self):
        pass

class BookWithPrint(Book, Printable):
    def print_details(self):
        print(f"Book: {self._model.title}, Author: {self._model.author}, Year: {self._model.year}")

class JournalWithPrint(Journal, Printable):
    def print_details(self):
        print(f"Journal: {self._model.title}, Author: {self._model.author}, Issue: {self.issue}, Year: {self._model.year}")


if __name__ == "__main__":
    library = Library()

    # Створення книги та журналу
    book_model = BookModel(title="1984", author="George Orwell", year=1949)
    book = BookWithPrint(book_model)

    journal_model = BookModel(title="Nature", author="Various", year=2021)
    journal = JournalWithPrint(journal_model, issue=102)

    # Додавання книг до бібліотеки
    library.add_book(book)
    library.add_book(journal)

    # Виведення списку книг у бібліотеці
    print("Library books:")
    print(library)

    # Виведення книг по імені автора
    print("\nBooks by George Orwell:")
    for book in library.books_by_author("George Orwell"):
        print(book)

    # Збереження списку книг у файл
    with LibraryFileManager("library.json", library):
        pass

    # Видалення книги з бібліотеки
    library.remove_book(book)

    # Виведення списку книг після видалення
    print("\nLibrary books after removing:")
    print(library)

    # Додавання книг з файлу в бібліотеку
    with LibraryFileManager("library.json", library):
        pass

    # Виведення списку книг після додавання з файлу
    print("\nLibrary books after loading from file:")
    print(library)
