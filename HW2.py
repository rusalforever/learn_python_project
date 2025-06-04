from pydantic import BaseModel
from contextlib import contextmanager
from abc import ABC, abstractmethod

class EBoooks(ABC): # абстрактний клас для всього що є в електронному форматі EBook
    @abstractmethod
    def inform(self):
        pass

class BookModel(BaseModel):
    title: str
    author: str
    year: int

class Book(EBoooks):
    def __init__(self, model: BookModel):
        self.model = model

    def inform(self):
        print(f'Book name: {self.model.title} written by {self.model.author} in {self.model.year}')

# декоратор для логування при доданні книги в список
def log_addition(func):
    def wrapper(self, book):
        len1 = len(self._book)
        result = func(self, book)
        len2 = len(self._book)
        if len2 > len1:
            print("New book added to library")
        else:
            print("Nothing added to the library")
        return result
    return wrapper

# декоратор який перевіряє наявність книги в бібліотеці перед її видаленням
def decorator(func):
    def wrapper(self, book_title):
        if book_title in [book.title for book in self._book]:
            return func(self, book_title)
        else:
            print(f'Book {book_title} is not in the list')
    return wrapper

#журнал:
class JournalModel(BookModel): # розширення pydentic BookModel для номеру журналу
    number: int

class Journal(Book):
    def __init__(self, model: JournalModel):
        super().__init__(model)
        self.number = model.number

    def inform(self): # додаємо в інформ номер журналу - поліморфізм
        print (f'Journal name: {self.model.title} written by {self.model.author} in {self.model.year}, issue number: {self.number}')

class Library:
    def __init__(self, _book: list[Book]):
        self._book = _book
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self._book):
            book = self._book[self.index]
            self.index += 1
            return book
        raise StopIteration

    @log_addition
    def add_book(self, book_title):
        if book_title not in self._book:
            self._book.append(book_title)

    @decorator  # бере як аргумент видалення книги зі списку
    def delete_book(self, book_title):
        self._book = [book for book in self._book if book_title != book_title]

if __name__ == "__main__":

    book1 = BookModel(title ='Fifth Risk', author = 'Michael Lewis', year = 2018)
    book2 = BookModel(title ='The World for Sale', author = 'Javier Blas', year = 2019)
    mag1 = JournalModel(title = 'Magaz', author = 'Nataliia', year = 2025, number=1)
    mag2 = JournalModel(title = 'The Oil Market', author = 'Javier Blas', year = 2025, number=2)

    Book(book1).inform()
    Journal(mag1).inform()

    book_lib = Library([])
    book_lib.add_book(book1)
    book_lib.add_book(book2)
    book_lib.add_book(mag1)
    book_lib.add_book(mag2)

for book in book_lib:
    print(f'Book list first run: {book}')


book_lib.delete_book("Fifth Risk")
for book in book_lib:
    print(f'Book list after removed books: {book}')


# генератор по автору

def generator(_book: list[Book], author_name: str):
    for book in _book:
        if book.model.author == author_name:
            yield book

for book in generator(book_lib._book, "Javier Blas"):
    print(f'Book title by Author: {book.model.title}')

# context manager
@contextmanager
def open_file(file, mode='w+r'):
    f = open(file, mode)
    yield f #збереження списку книг до файлу
    f.close()

with open_file('library.txt', 'w') as f:
    for book in book_lib:
        f.write(str(book) + '\n')

with open_file('library.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(f'Read with context manager: {line.strip()}')





