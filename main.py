from lib.models import Book, BookModel, Magazine
from lib.library import Library
from lib import storage

FILE_NAME = "test.json"


def print_books(library: Library):
    print("===============")
    for book in library:
        print(f"Book: {book}")


if __name__ == '__main__':
    library = Library([])

    book1 = Book(BookModel(title="To Kill a Mockingbird", author="Harper Lee",
                           year=1960))
    book2 = Book(BookModel(title="1984", author="George Orwell",
                           year=1949))
    book3 = Book(
        BookModel(title="The Great Gatsby", author="F. Scott Fitzgerald",
                  year=1925))

    magazine1 = Magazine(
        BookModel(title="National Geographic", author="Multiple Authors",
                  year=2020))
    magazine2 = Magazine(BookModel(title="Time", author="Multiple Authors",
                                   year=2021))

    library.add(book1)
    library.add(book2)
    library.add(book3)
    library.add(magazine1)
    library.add(magazine2)

    print_books(library)

    print("=========")
    for book in library.books_by_author("Multiple Authors"):
        print(f"Multiple Authors: {book}")

    storage.save(library, FILE_NAME)

    library.remove(magazine2)
    print_books(library)

    storage.load(library, FILE_NAME)
    print_books(library)