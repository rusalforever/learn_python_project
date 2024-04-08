import json
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


def loger_add_book(func):
    def wrapper(*args, **kwargs):
        item = kwargs.get('item')
        print(f'Adding item -> {item.item_info()}')
        result = func(*args, **kwargs)
        return result

    return wrapper


def check_book_existence(func):
    def wrapper(library, title):
        for item in library.items:
            if item.model.title == title:
                return func(library, title)
        print(f"Item '{title}' not found in the library.")

    return wrapper


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class JournalModel(BookModel):
    edition: int


class AbstractLibraryItem(ABC):
    def __init__(self, model: BaseModel):
        self.model = model

    @abstractmethod
    def item_info(self):
        raise NotImplementedError


class Book(AbstractLibraryItem):
    def item_info(self):
        return f"Title: {self.model.title}, Author: {self.model.author}, Year: {self.model.year}"


class Journal(AbstractLibraryItem):
    def item_info(self):
        return (f"Title: {self.model.title}, Author: {self.model.author}, Year: {self.model.year}, "
                f"Edition: {self.model.edition}")


class Library:
    def __init__(self, items: List[AbstractLibraryItem] = None):
        self._items = items if items else []

    @property
    def items(self):
        return self._items

    @loger_add_book
    def add_item(self, item: AbstractLibraryItem):
        self._items.append(item)

    @check_book_existence
    def remove_item(self, title: str):
        for item in self._items:
            if item.model.title == title:
                self._items.remove(item)
                print(f"Item '{title}' removed from the library.")
                return

    def get_items_by_author(self, author: str):
        return (item for item in self._items if item.model.author == author)

    def list_items(self):
        for item in self._items:
            print(item.item_info())

    def save_to_file(self, filename: str):
        with open(filename, 'w') as file:
            data = [item.model.model_dump() for item in self._items]
            json.dump(data, file)
        print(f"Library saved to {filename}")

    def load_from_file(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item_data in data:
                if 'edition' in item_data:
                    model = JournalModel(**item_data)
                    item = Journal(model)
                else:
                    model = BookModel(**item_data)
                    item = Book(model)
                self._items.append(item)
        print(f"Library loaded from {filename}")


if __name__ == '__main__':
    library = Library()
    book_model = BookModel(title="Book1", author="Author1", year=2008)
    book = Book(model=book_model)

    journal_model = JournalModel(title="Journal1", author="Author2", year=2005, edition=2)
    journal = Journal(model=journal_model)

    library.add_item(item=book)
    library.add_item(item=journal)

    print()
    print("Listing all items in the library:")
    library.list_items()

    print("\nListing items by Author1:")
    author1_items = library.get_items_by_author("Author1")
    for item in author1_items:
        print(item.item_info())

    print("\nRemoving item 'Book1'")
    library.remove_item(title="Book1")

    print("\nRemoving item 'Book1' again to check @check_book_existence message")
    library.remove_item(title="Book1")

    print("\nListing items after removal:")
    library.list_items()

    print("\nSaving library to file 'library.json'")
    library.save_to_file("library.json")

    print("\nLoading library from file 'LIBRARY.json'")
    library.load_from_file("LIBRARY.json")

    print("\nListing items after loading from file:")
    library.list_items()
