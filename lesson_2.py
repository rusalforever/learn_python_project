from typing import List
from pydantic import BaseModel
import logging
import json


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class AbstractLibraryItem(BaseModel):
    def item_info(self):
        raise NotImplementedError


class Book(BookModel, AbstractLibraryItem):
    def item_info(self):
        return f"Книга '{self.title}' автора {self.author}, год издания {self.year}"


class Journal(BaseModel):
    title: str
    author: str
    year: int
    edition: int

    def item_info(self):
        return f"Журнал '{self.title}' автора {self.author}, год издания {self.year}, номер издания {self.edition}"


class Library:
    def __init__(self):
        self.__books: List[AbstractLibraryItem] = []

    def __iter__(self):
        return iter(self.__books)

    def book_author(self, author: str):
        return [book for book in self.__books if isinstance(book, Book) and book.author.lower() == author.lower()]

    @staticmethod
    def log_add_book(func):
        def wrapper(self, item: AbstractLibraryItem):
            logging.info(f"Добавлено в библиотеку: {item.item_info()}")
            return func(self, item)

        return wrapper

    @staticmethod
    def check_book_exists(func):
        def wrapper(self, title: str):
            if any(isinstance(book, Book) and book.title.lower() == title.lower() for book in self.__books):
                return func(self, title)
            else:
                logging.error(f"Книга '{title}' не найдена в библиотеке.")

        return wrapper

    @log_add_book
    def add_book(self, item: AbstractLibraryItem):
        self.__books.append(item)

    @check_book_exists
    def remove_book(self, title: str):
        self.__books = [book for book in self.__books if
                        not (isinstance(book, Book) and book.title.lower() == title.lower())]

    def save_books(self, filename: str = 'my_file.txt'):
        unique_books = set()
        unique_journals = set()

        with open(filename, 'w') as file:
            for item in self.__books:
                if isinstance(item, Book):
                    book_tuple = (item.title, item.author, item.year)
                    if book_tuple not in unique_books:
                        unique_books.add(book_tuple)
                        file.write(f"Книга: {item.title}, Автор: {item.author}, Год издания: {item.year}\n")
                elif isinstance(item, Journal):
                    journal_tuple = (item.title, item.author, item.year, item.edition)
                    if journal_tuple not in unique_journals:
                        unique_journals.add(journal_tuple)
                        file.write(
                            f"Журнал: {item.title}, Автор: {item.author}, Год издания: {item.year}, Номер издания: {item.edition}\n")

    def load_books_from_file(self, filename: str = 'book.json'):
        with open(filename, 'r') as file:
            books_data = json.load(file)
            for book_data in books_data:
                if 'edition' in book_data:
                    journal = Journal(**book_data)
                    self.add_book(journal)
                else:
                    book = Book(**book_data)
                    self.add_book(book)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    my_library = Library()

    my_library.load_books_from_file()

    books_in_library = list(my_library)
    if books_in_library:
        print("Список книг в библиотеке:")
        for item in books_in_library:
            print(item.item_info())

    author = "Вильям Шекспир"
    book_author = my_library.book_author(author)
    if book_author:
        print(f"\nКниги автора '{author}':")
        for book in book_author:
            print(book.item_info())

    title_to_remove = "Гамлет"
    my_library.remove_book(title_to_remove)
    books_after_removal = list(my_library)
    if books_after_removal:
        print("\nУдалена книга:", {title_to_remove})
        print("Список книг после удаления:")
        for item in books_after_removal:
            print(item.item_info())

    my_library.load_books_from_file('book.json')
    books_after_addition = list(my_library)
    if books_after_addition:
        print("\nСписок книг в библиотеке после добавления:")
        for item in books_after_addition:
            print(item.item_info())

    my_library.save_books('my_file.txt')
