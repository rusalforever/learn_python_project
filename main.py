import json
from typing import List
from pydantic import BaseModel
from abc import ABC, abstractmethod

# ps возможно немного заигрался...

def validate_json_path(func):
    def wrapper(self, *args, **kwargs):
        if not self.path.endswith(".json"):
            raise ValueError(f"path must end with '.json'.")
        return func(self, *args, **kwargs)
    return wrapper

def handle_publish(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'New Publish: {result}')
        return result
    return wrapper

class FileHandler(BaseModel, ABC):
    path: str

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

class JsonHandler(FileHandler):

    @validate_json_path
    def save(self, data: any):
        with open(self.path, 'w') as f:
            json.dump(data, f)

    @validate_json_path
    def load(self):
        with open(self.path, 'r') as f:
            return json.load(f)

class BookModel(BaseModel, ABC):
    title: str
    author: str
    year: int

    @abstractmethod
    def get_info(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.get_info()

class Book(BookModel):

    def get_info(self):
        return f"Book(title={self.title!r}, author={self.author!r}, year={self.year!r})"

class Journal(Book):

    def get_info(self):
        return f"Journal(title={self.title!r}, author={self.author!r}, year={self.year!r})"

class Library(BaseModel):
    _books: List[Book] = []
    current_book: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_book < len(self._books):
            book = self._books[self.current_book]
            self.current_book += 1
            return book
        else:
            raise StopIteration

    def delete_item(self, book: Book):
        self._books.remove(book)

    @handle_publish
    def add_item(self, book: Book):
        self._books.append(book)
        return book

    def get_items(self) -> List[Book]:
        return self._books

    def get_items_by_author(self, author: str):
        return list(filter(lambda book: book.author.lower() == author.lower(), self._books))


    def save_to_file(self, path: str):
        j = JsonHandler(path=path)
        result = []

        # такий ж самий вормат json, як у extra_books
        for book in self._books:
            book_json = book.model_dump()
            book_json['type'] = book.__class__.__name__
            result.append(book_json)

        j.save(result)


    def add_from_file(self, path: str):
        j = JsonHandler(path=path)
        data = j.load()
        for book in data:
            try:
                book_type = book.get('type', '').lower()
                if book_type == 'book':
                    b = Book(
                        title=book.get('title', ''),
                        author=book.get('author', ''),
                        year=book.get('year', ''),
                    )
                    self._books.append(b)
                elif book_type == 'journal':
                    j = Journal(
                        title=book.get('title', ''),
                        author=book.get('author', ''),
                        year=book.get('year', ''),
                    )
                    self._books.append(j)
                else:
                    raise Exception(f'Unknown book type: {book_type}')
            except Exception as e:
                print(f'Skipping {book} due to {e}')

# створення бібліотеки
library = Library()

# створення інстансу книги та журналу
test_book = Book(title='Book Title', author='Author 1', year=2020)
test_journal = Journal(title='Journal Title', author='Author 2', year=2020)

# додавання їх у бібліотеку
library.add_item(test_book)
library.add_item(test_journal)

print(f"\nвиведення списку книг у бібліотеці \n{library.get_items()}\n")

print(f"виведення списку книг бібліотеки по імені автора \n{library.get_items_by_author('author 1')}\n")

# збереження списку книг у файл
library.save_to_file('some_file.json')

# видалення книги з бібліотеки
library.delete_item(test_book)

print(f'виведення списку книг після видалення \n{library.get_items()}\n')

# додавання книг з файлу в бібліотеку
library.add_from_file('extra_books.json')

print(f'виведення списку книг бібліотеки після додавання p файлу \n{library.get_items()}')
