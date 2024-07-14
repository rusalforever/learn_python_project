from library_management.book_model import BookModel
from library_management.book import Book
from library_management.library import Library
from library_management.context_manager import save_books_to_file, load_books_from_file
from library_management.journal import Journal

if __name__ == "__main__":
    library = Library()

    book1 = Book(BookModel(title="Book One", author="Author A", year_of_publication=2001))
    book2 = Journal(BookModel(title="Journal One", author="Author B", year_of_publication=2005), issue_number=1)

    library.add_book(book1)
    library.add_book(book2)

    print("List of books in the library:")
    for book in library:
        print(book.get_ribbon())

    print("\nBooks by Author A:")
    for book in library.books_by_author("Author A"):
        print(book.get_ribbon())

    save_books_to_file(library, "library_books.json")

    library.remove_book(book1)

    print("\nList of books after deletion:")
    for book in library:
        print(book.get_ribbon())

    load_books_from_file(library, "library_books.json")

    print("\nList of books after loading from file:")
    for book in library:
        print(book.get_ribbon())
