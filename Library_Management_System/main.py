from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import List, Iterator, Type
import json


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class Publication(ABC):
    @abstractmethod
    def display_info(self) -> str:
        pass


# Decorator for logging actions
def log_action(action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Action: {action} - {args[1].display_info()}")
            return result

        return wrapper

    return decorator


# Decorator for checking book existence
def check_existence(func):
    def wrapper(self, book):
        if book not in self._books:
            print("Error: Book not found in the library.")
            return
        return func(self, book)

    return wrapper


class Book(Publication):
    def __init__(self, model: BookModel):
        self.model = model

    def display_info(self) -> str:
        return f"Title: {self.model.title.title()}\nAuthor: {self.model.author.title()}\nYear: {self.model.year}"


class Magazine(Book):
    def __init__(self, model, issue_number):
        super().__init__(model)
        self.issue_number = issue_number

    def display_info(self) -> str:
        info = super().display_info()
        return f"{info}\nIssue: {self.issue_number}"


class Library:
    def __init__(self):
        self.__books: List[Publication] = []

    def __iter__(self) -> Iterator[Publication]:
        self._index = 0
        return self

    def __next__(self) -> Publication:
        if self._index < len(self.__books):
            book = self.__books[self._index]
            self._index += 1
            return book
        else:
            raise StopIteration

    def find_by_author(self, author: str) -> List[str]:
        matching_books = [book.display_info() for book in self.__books if book.model.author.lower() == author.lower()]
        return matching_books

    @log_action("Added")
    def add_book(self, book: Publication) -> None:
        self.__books.append(book)

    @check_existence
    @log_action("Removed")
    def remove_book(self, book: Publication) -> None:
        self.__books.remove(book)

    def display_books(self) -> None:
        for book in self.__books:
            print(book.display_info())

    def display_books_by_author(self, author: str) -> None:
        books_by_author = self.find_by_author(author)
        if books_by_author:
            print(f"Books by the author {author}:")
            for book in books_by_author:
                print(book)
        else:
            print(f"No books by {author} have been found in the library.")


class LibraryFileManager:
    def __init__(self, library: Library, filename: str):
        self.library = library
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def save(self) -> None:
        with open(self.filename, 'w') as file:
            data = [book.model.dict() for book in self.library._Library__books]  # Use mangled name
            json.dump(data, file)

    def load(self) -> None:
        with open(self.filename, 'r') as file:
            data = json.load(file)
            for item in data:
                if 'issue_number' in item:
                    self.library.add_book(Magazine(BookModel(**item), item['issue_number']))
                else:
                    self.library.add_book(Book(BookModel(**item)))


if __name__ == "__main__":
    library = Library()

    first_book = Book(BookModel(
        title="Лісова Пісня",
        author="Леся Українка",
        year=1911))
    second_book = Book(BookModel(
        title="Тіні Забутих Предків",
        author="Михайло Коцюбинський",
        year=1912))
    magazine = Magazine(BookModel(
        title="National Geographic",
        author="National Geographic Society",
        year=2022),
        issue_number=6)

    library.add_book(first_book)
    library.add_book(second_book)
    library.add_book(magazine)
    print("\n")

    # Display all books in the library
    library.display_books()
    print("\n")


    # Display books by author "Леся Українка"
    library.display_books_by_author("Леся Українка")
    print()

    # Use context manager to save and load books
    with LibraryFileManager(library, 'library.json') as manager:
        manager.save()

    print("Books after saving and loading:")
    library = Library()
    with LibraryFileManager(library, 'library.json') as manager:
        manager.load()
        library.display_books()
