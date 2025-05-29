from typing import List, Generator
import logging
from .book import Book
from .comics import Comics

logging.basicConfig(level=logging.INFO)

def log_addition(func):
    def wrapper(library, book):
        logging.info(f"Adding book: {book.get_ribbon()}")
        return func(library, book)
    return wrapper

def check_book_exists(func):
    def wrapper(library, book):
        if book not in library._books:
            raise ValueError("Book not found in the library")
        return func(library, book)
    return wrapper

class Library:
    def __init__(self):
        self._books: List[Book] = []
        self.initialize_starter_books()

    def initialize_starter_books(self):
        starter_books = [
            Book(title="Кайдашева сім'я", author="Іван Семенович Нечуй-Левицький"),
            Book(title="Лісова пісня", author="Леся Українка"),
            Comics(title="Star Wars Knights of the Old Republic 43: The Reaping, Part 1", author="John Jackson Miller", illustrator="Dustin Weaver", series="Star Wars: Knights of the Old Republic"),
            Comics(title="Unseen, Unheard", author="Chris Avellone", illustrator="Dustin Weaver", series="Star Wars Tales")
        ]
        self._books.extend(starter_books)

    @log_addition
    def add_book(self, book: Book):
        self._books.append(book)

    @check_book_exists
    def remove_book(self, book: Book):
        self._books.remove(book)

    def __iter__(self):
        return iter(self._books)

    def books_by_author(self, author: str) -> Generator[Book, None, None]:
        return (book for book in self._books if book._book_model.author == author)
