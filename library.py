from typing import List, Generator
from functools import wraps
import logging
import json
import os
from contextlib import contextmanager

from models import BookModel, MagazineModel, LibraryItemModel


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_item_addition(func):
    """
    Decorator to log book addition
    """

    @wraps(func)
    def wrapper(self, item: BookModel, *args, **kwargs):

        logging.info(f"Adding {'book' if item.type == 'book' else 'magazine'} to library: '{item.title}' by {item.author}")


        result = func(self, item, *args, **kwargs)


        logging.info(f"{'book' if item.type == 'book' else 'magazine'} successfully added. Total items in library: {len(self._items)}")

        return result

    return wrapper


def check_book_exists(func):
    """
    Decorator to check if a book exists
    """

    @wraps(func)
    def wrapper(self, item: BookModel, *args, **kwargs):

        if item not in self._items:
            logging.warning(f"Book '{item.title}' by {item.author} not found in library")
            raise ValueError(f"Book '{item.title}' by {item.author} is not in the library")


        logging.info(f"Removing book from library: '{item.title}' by {item.author}")


        result = func(self, item, *args, **kwargs)


        logging.info(f"Book successfully removed. Total books in library: {len(self._items)}")

        return result

    return wrapper

class Library:
    """
    Class representing a library
    """
    def __init__(self) -> None:
        """
        Initializes the library with an empty list of books
        """
        self._items: List[LibraryItemModel] = []
        self._current_book_index = 0

    @property
    def books(self) -> str:
        """
        Returns copy of the list of books
        """
        return "/n".join([str(item) for item in self._items if isinstance(item, BookModel)])


    def magazines(self) -> str:
        """
        Returns copy of the list of magazines
        """
        return "/n".join([str(item) for item in self._items if isinstance(item, MagazineModel)])

    def all_library_items(self) -> List[LibraryItemModel]:
        return list(self._items)

    def __str__(self):
        """
        Returns a string representation of the library
        """
        if not self._items:
            return "No libray items available"

        return f"Library of {len(self._items)} books"

    def __iter__(self):
        self._current_item_index = 0
        return self

    def get_books_by_author(self, author_name: str) -> Generator[BookModel, None, None]:
        """
        Generator that yields books by a specific author

        Args:
            author_name (str): Name of the author to search for

        Yields:
            BookModel: Books written by the specified author
        """
        for book in self._items:
            if isinstance(book, BookModel) and book.author.lower() == author_name.lower():
                yield book

    def __next__(self):
        if self._current_item_index < len(self._items):
            book = self._items[self._current_item_index]
            self._current_item_index += 1
            return book
        else:
            self._current_item_index = 0
            raise StopIteration

    @log_item_addition
    def add_item(self, item: LibraryItemModel) -> None:
        """
        Adds an item to the library
        """
        self._items.append(item)

    @check_book_exists
    def remove_item(self, item: LibraryItemModel) -> None:
        """
        Removes a book from the library

        Args:
            book (BookModel): Book to remove from the library

        Raises:
            ValueError: If the book is not found in the library
            :param item:
        """
        self._items.remove(item)

    def to_dict(self) -> dict:
        """
        Converts the library to a dictionary for serialization

        Returns:
            dict: Dictionary representation of the library
        """
        return {
            'items': [
                {
                    'type': 'magazine' if isinstance(item, MagazineModel) else 'book',
                    'title': item.title,
                    'author': item.author,
                    'year': item.year,
                    **({'issue': item.issue, 'month': item.month} if isinstance(item, MagazineModel) else {})

                }
                for item in self._items
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Library':
        """
        Creates a library instance from a dictionary

        Args:
            data (dict): Dictionary containing library data

        Returns:
            Library: New library instance with loaded books
        """
        library = cls()
        for item_data in data.get('items', []):
            if item_data.get('type') == 'magazine':
                item = MagazineModel(
                    type=item_data.get('type'),
                    title=item_data['title'],
                    author=item_data['author'],
                    year=item_data['year'],
                    issue=item_data['issue'],
                    month=item_data['month']
                )
            else:
                item = BookModel(
                    type=item_data['type'],
                    title=item_data['title'],
                    author=item_data['author'],
                    year=item_data['year']
                )
            library._items.append(item)
        return library

    @contextmanager
    def file_manager(self, filename: str, mode: str = 'r'):
        """
        Context manager for file operations with the library
        """
        try:
            if mode == 'r' and os.path.exists(filename):
                logging.info(f"Loading library from file: {filename}")
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        loaded_library = Library.from_dict(data)
                        self._items = loaded_library._items
                        logging.info(f"Successfully loaded {len(self._items)} books from {filename}")
                except (json.JSONDecodeError, KeyError) as e:
                    logging.error(f"Error loading library from {filename}: {e}")
                    raise
            elif mode == 'r' and not os.path.exists(filename):
                logging.warning(f"File {filename} does not exist. Starting with empty library.")

            yield self

        except Exception as e:
            logging.error(f"Error in file operation: {e}")
            raise
        finally:
            if mode == 'w':
                logging.info(f"Saving library to file: {filename}")
                try:
                    os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
                    with open(filename, 'w', encoding='utf-8') as file:
                        json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)
                        logging.info(f"Successfully saved {len(self._items)} books to {filename}")
                except Exception as e:
                    logging.error(f"Error saving library to {filename}: {e}")
                    raise
