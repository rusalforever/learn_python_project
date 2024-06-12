from abc import ABC, abstractmethod
from typing import List, Generator
from pydantic import BaseModel
import logging
import json


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class AbstractLibraryItem(ABC):
    def __init__(self):
        self.title = None

    @abstractmethod
    def item_info(self) -> str:
        pass


class BookInfo(BookModel, AbstractLibraryItem):
    def item_info(self) -> str:
        return f"Книга '{self.title}' автора {self.author}, год издания {self.year}"


class Journal(BaseModel, AbstractLibraryItem):
    title: str
    author: str
    year: int
    release: int

    def item_info(self) -> str:
        return f"Журнал '{self.title}' автора {self.author}, год издания {self.year}, выпуск {self.release}"


def log_add_book(func):
    def wrapper(self, items: AbstractLibraryItem):
        logging.info(f"Добавлено в библиотеку: {items.item_info()}")
        return func(self, items)

    return wrapper


def check_book_exists(func):
    def wrapper(self, title: str):
        if any(book.title.lower() == title.lower() for book in self._books):
            return func(self, title)
        else:
            logging.error(f"Книга '{title}' не найдена в библиотеке.")
            return None

    return wrapper


class LibraryFileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class Library:
    def __init__(self):
        self._books: List[AbstractLibraryItem] = []

    def __iter__(self) -> Generator[AbstractLibraryItem, None, None]:
        for book in self._books:
            yield book

    @log_add_book
    def add_book(self, item: AbstractLibraryItem):
        self._books.append(item)

    @check_book_exists
    def remove_book(self, title: str):
        self._books = [book for book in self._books if book.title.lower() != title.lower()]

    def save_books(self, filename: str = 'my_library.txt'):
        with LibraryFileManager(filename, 'w') as file:
            for item in self._books:
                file.write(f"{item.item_info()}\n")

    def load_books_from_file(self, filename: str = 'library.json'):
        with LibraryFileManager(filename, 'r') as file:
            try:
                books_data = json.load(file)
                for book_data in books_data:
                    if 'release' in book_data:
                        journal = Journal(**book_data)
                        self.add_book(journal)
                    else:
                        book_info = BookInfo(**book_data)
                        self.add_book(book_info)
            except json.JSONDecodeError as e:
                logging.error(f"Помилка при завантаженні даних: {e}")


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    my_library = Library()
    my_library.load_books_from_file()

    print("Список книг и журналов в библиотеке после загрузки из файла:")
    for item in my_library:
        print(item.item_info())

    my_library.remove_book("Война миров")
    print("\nПосле удаления книги 'Война миров':")
    for item in my_library:
        print(item.item_info())

    my_library.save_books('my_library.txt')