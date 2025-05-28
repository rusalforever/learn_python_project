from pydantic import BaseModel
import json


# Decorators
def log_book_addition(func):
    def wrapper(self, book, *args, **kwargs):
        if isinstance(book, Book):
            print(f"[BOOK_ADDITION] Додання книги: '{book.name}' (Автор: {book.author}, Рік: {book.year})")
            return func(self, book, *args, **kwargs)
        return None

    return wrapper

def check_book_exists_before_removal(func):
    def wrapper(self, book_to_remove, *args, **kwargs):
        if not isinstance(book_to_remove, Book):
            return None

        if book_to_remove in self._books:
            print(f"[BOOK_REMOVAL] Книга '{book_to_remove.name}' ({book_to_remove.author}) існує. Спроба видалення...")
            return func(self, book_to_remove, *args, **kwargs)
        else:
            print(f"[BOOK_REMOVAL_ERROR] Книгу '{book_to_remove.name}' ({book_to_remove.author}) не знайдено в бібліотеці.")
            return None
    return wrapper

def check_book_exists_before_addition(func):
    def wrapper(self, book, *args, **kwargs):
        if not isinstance(book, Book):
            print(
                f"[BOOK_ADDITION_ERROR] Об'єкт даного типу неможливо додати до бібліотеки ({type(book)}).")
            return None

        if book in self._books:
            print(f"[BOOK_ADDITION_ERROR] Книга '{book.name}' ({book.author}) вже є в бібліотеці.")
            return None
        else:
            return func(self, book, *args, **kwargs)
    return wrapper


# Classes
class BookModel(BaseModel):
    title: str
    author: str
    year: int


class Book:
    @property
    def name(self) -> str:
        return self._book_data.title

    @property
    def author(self) -> str:
        return self._book_data.author

    @property
    def year(self) -> int:
        return self._book_data.year

    def __init__(self, book_data: BookModel):
        self._book_data = book_data

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.name == other.name and
                self.author == other.author and
                self.year == other.year)

    def __hash__(self):
        return hash((self.name, self.author, self.year))

    def __repr__(self) -> str:
        return f"(title='{self.name}', author='{self.author}', year={self.year})"

    def get_info(self) -> str:
        return (f"Назва: {self.name}\n"
                f"Автор: {self.author}\n"
                f"Рік видання: {self.year}")


class Library:
    def __init__(self, books: list[Book] = None):
        if books is None:
            self._books: list[Book] = []
        else:
            self._books: list[Book] = list(books)

    # iterator
    def __iter__(self):
        return iter(self._books)

    def __str__(self) -> str:
        if not self._books:
            return "Бібліотека порожня."

        return f"Книги в бібліотеці: ({len(self._books)} шт.)"

    # generator
    def get_books_by_author(self, author_name: str):
        found_any = False
        for book in self._books:
            if book.author == author_name:
                yield book
                found_any = True
        if not found_any:
            print(f"Книг автора '{author_name}' не знайдено.")

    @check_book_exists_before_addition
    @log_book_addition
    def add_book(self, book: Book):
        self._books.append(book)

    @check_book_exists_before_removal
    def remove_book(self, book_to_remove: Book):
        self._books.remove(book_to_remove)
        print(f"Книгу '{book_to_remove.name}' ({book_to_remove.author}) видалено з бібліотеки.")

    def get_books(self) -> list[Book]:
        # Повертаємо копію списку книг
        return self._books[:]

    def import_from_file(self, path: str):
        with FileOpener(path, 'r') as file:
            try:
                for line in file:
                    try:
                        book_data = json.loads(line.strip())
                        book_model = BookModel(**book_data)
                        book = Book(book_model)
                        self.add_book(book)
                    except json.JSONDecodeError:
                        print(f"[IMPORT_ERROR] Неправильний формат JSON в рядку: {line}")
                    except Exception as e:
                        print(f"[IMPORT_ERROR] Помилка при імпорті книги: {e}")
            except Exception as e:
                print(f"[IMPORT_ERROR] Помилка при читанні файлу: {e}")

    def export_to_file(self, path: str):
        with FileOpener(path, 'w') as file:
            try:
                for book in self._books:
                    book_data = {
                        "title": book.name,
                        "author": book.author,
                        "year": book.year
                    }
                    json_line = json.dumps(book_data, ensure_ascii=False)
                    file.write(json_line + '\n')
            except Exception as e:
                print(f"[EXPORT_ERROR] Помилка при експорті книг: {e}")


class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


