import logging


def book_added_log(func):
    def wrapper(library, book):
        res = func(library, book)
        logging.info(f"The book has added: {book.get_ribbon()}")
        return res
    return wrapper


def book_exists(func):
    def wrapper(library, book):
        if book not in library.books:
            raise ValueError("Book not exists")
        return func(library, book)
    return wrapper
