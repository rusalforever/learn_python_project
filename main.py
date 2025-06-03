from pydantic import BaseModel
from abc import ABC, abstractmethod

class BookModel(BaseModel):
    title: str
    author: str
    year: int

class MagazineModel(BaseModel):
    name: str
    number: int
    month: str
    year: int

class Publication(ABC):
    @abstractmethod
    def show_author(self):
        pass

class Book(Publication):
    def __init__(self, model: BookModel):
        self.__model = model

    def __str__(self):
        return f"{self.__model.title} by {self.__model.author} in {self.__model.year}"

    def show_author(self) -> str:
        return self.__model.author

class Magazine(Publication):
    def __init__(self, model: MagazineModel):
        self.__model = model

    def __str__(self):
        return f"{self.__model.name} #{self.__model.number} / {self.__model.month} in {self.__model.year}"

    def show_author(self) -> str:
        return self.__model.name

class Library:
    def __init__(self, book_list: list[Book]):
        self.books = book_list
        self.current_book = 0

    def __iter__(self):
        self.current_book = 0

        return self

    def __next__(self):
        if self.current_book >= len(self.books):
            raise StopIteration

        b = self.books[self.current_book]
        self.current_book += 1

        return b

    def book_generator(self, author):
        for b in self.books:
            if b.show_author() == author:
                yield b

    def add_book(self, b: Book):
        self.books.append(b)

    def remove_book(self, b: Book):
        self.books.remove(b)

    def save_to_file(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            for book in self.books:
                f.write(str(book) + "\n")

    @staticmethod
    def load_from_file(filename: str):
        books = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if " by " in line and " in " in line:
                    try:
                        title_part, rest = line.split(" by ", 1)
                        author_part, year_part = rest.rsplit(" in ", 1)

                        title = title_part.strip()
                        author = author_part.strip()
                        year = int(year_part.strip())
                        model = BookModel(title=title, author=author, year=year)
                        books.append(Book(model))
                    except ValueError:
                        print(f"Failed to parse line: {line}")
                elif " #" in line and " / " and " in " in line:
                    try:
                        name_part, rest = line.split(" #", 1)
                        number_part, rest = rest.split(" / ", 1)
                        month_part, year_part = rest.rsplit(" in ", 1)

                        name = name_part.strip()
                        number = int(number_part.strip())
                        month = month_part.strip()
                        year = int(year_part.strip())

                        model = MagazineModel(name=name, number=number, month=month, year=year)
                        books.append(Magazine(model))
                    except ValueError:
                        print(f"Failed to parse line: {line}")
                else:
                    print(f"Invalid format: {line}")
        return books

def add_book_generator(func):
    def wrapper(book, library, *args, **kwargs):
        print(f"Adding book...")
        result = func(book, library, *args, **kwargs)
        print(f"Book {book} added to library")
        print("[BOOKS IN LIBRARY]")
        for b in library.books:
            print(b)

        return result
    return wrapper

@add_book_generator
def add_book_library(book: Book, library: Library):
    library.add_book(book)

def remove_book_generator(func):
    def wrapper(book, library, *args, **kwargs):
        if book not in library.books:
            print(f"Book {book} not found in library!")

            return None

        print(f"Removing book...")
        result = func(book, library, *args, **kwargs)
        print(f"Book removed from library")
        print("[BOOKS IN LIBRARY]")
        for b in library.books:
            print(b)

        return result
    return wrapper

@remove_book_generator
def remove_book_library(book, library):
    library.remove_book(book)

book1 = Book(BookModel(title="Ubik", author="Philip K. Dick", year=1966))
book2 = Book(BookModel(title="The Man in the High Castle", author="Philip K. Dick", year=1962))
book3 = Book(BookModel(title="The colour of magic", author="Terry Pratchett", year=1983))
book4 = Book(BookModel(title="Mort", author="Terry Pratchett", year=1987))

magazine1 = Magazine(MagazineModel(name="Nintendo Power", number=13, month="January", year=1989))
magazine2 = Magazine(MagazineModel(name="Pepper", number=21, month="June", year=1995))

myBooks = Library([book1, book2, book3, magazine1, magazine2])

print(next(myBooks))
print(next(myBooks))
print(next(myBooks))

print("\n[ADD BOOKS TO LIBRARY]")
add_book_library(book4, myBooks)

print(next(myBooks))

remove_book_library(book1, myBooks)

myBooks.save_to_file("log.txt")

print("\n[LOAD FROM FILE]")
r = myBooks.load_from_file("log.txt")

for book in r:
    print(book.show_author())