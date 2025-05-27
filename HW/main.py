from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Generator, Iterator
from contextlib import contextmanager
import logging
import json

# Налаштування логування у файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="library.log",
    filemode="a",       # додаємо до існуючого
    encoding="utf-8",   # для української мови
)
logger = logging.getLogger(__name__)

# Pydantic-модель
class BookModel(BaseModel):
    title: str
    author: str
    year: int
    type: str


# Абстрактний клас Publication
class Publication(ABC):
    def __init__(self, model: BookModel) -> None:
        self._model = model

    @property
    def model(self) -> BookModel:
        return self._model

    @abstractmethod
    def info(self) -> str:
        pass


# Клас Book
class Book(Publication):
    def info(self) -> str:
        return f"Книга: '{self.model.title}', автор: {self.model.author}, рік: {self.model.year}"


# Клас Journal
class Journal(Publication):
    def info(self) -> str:
        return f"Журнал: '{self.model.title}', автор: {self.model.author}, рік: {self.model.year}"


# Декоратор для логування
def log_action(func):
    def wrapper(self, book: Publication):
        logger.info(f"[LOG] Додаємо публікацію: {book.model.title}")
        return func(self, book)
    return wrapper


# Декоратор для перевірки перед видаленням
def check_book_exists(func):
    def wrapper(self, title: str):
        if not any(b.model.title == title for b in self._books):
            logger.warning(f"[WARNING] Публікація '{title}' не знайдена в бібліотеці.")
            return
        return func(self, title)
    return wrapper


# Клас Library
class Library:
    def __init__(self):
        self._books: list[Publication] = []

    @log_action
    def add_book(self, book: Publication) -> None:
        self._books.append(book)

    # Внутрішній метод без логування (для завантаження з файлу)
    def _add_book_directly(self, book: Publication) -> None:
        self._books.append(book)

    @check_book_exists
    def remove_book(self, title: str) -> None:
        self._books = [b for b in self._books if b.model.title != title]
        logger.info(f"[INFO] Публікацію '{title}' видалено з бібліотеки.")

    def __iter__(self) -> Iterator[Publication]:
        return iter(self._books)

    def books_by_author(self, author: str) -> Generator[Publication, None, None]:
        return (b for b in self._books if b.model.author == author)

    def save_to_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {**b.model.model_dump(), "type": "journal" if isinstance(b, Journal) else "book"}
                    for b in self._books
                ],
                f,
                ensure_ascii=False,
                indent=4
            )
        logger.info(f"[INFO] Бібліотека збережена у файл '{filename}'.")

    def load_from_file(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._books.clear()
            for item in data:
                if item["type"] == "journal":
                    self._add_book_directly(Journal(BookModel(**item)))
                else:
                    self._add_book_directly(Book(BookModel(**item)))
        logger.info(f"[INFO] Бібліотека завантажена з файлу '{filename}'.")


# Контекстний менеджер
@contextmanager
def LibraryFileManager(library: Library, filename: str):
    try:
        library.load_from_file(filename)
        yield library
    finally:
        library.save_to_file(filename)
        logger.info(f"[INFO] Завершено роботу з файлом бібліотеки.")

# ============================================================================

# Основний блок
if __name__ == "__main__":
    lib = Library()

    # Створення книги та журналу
    book_01 = Book(BookModel(title="Мистецтво війни", author="Сунь-Цзи", year=500, type="book"))
    journal_01 = Journal(BookModel(title="Науковий журнал", author="Іван Іванов", year=2024, type="journal"))
    book_02 = Book(BookModel(title="Берестечко", author="Ліна Костенко", year=2010, type="book"))
    book_03 = Book(BookModel(title="Сад нетанучих скульптур", author="Ліна Костенко", year=2019, type="book"))

    # Додавання
    lib.add_book(book_01)
    lib.add_book(journal_01)
    lib.add_book(book_02)
    lib.add_book(book_03)
    
    # Видалення книги з пам'яті (RAM) без збереження у файл
    lib.remove_book("Мистецтво війни")
    print("\nСписок публікацій після видалення книги з пам'яті (без збереження у файл):")
    for pub in lib:
        print(pub.info())

    # Збереження до файлу
    lib.save_to_file("library.json")
    
    # Виведення всіх публікацій
    print("\nСписок всіх публікацій:")
    for pub in lib:
        print(pub.info())

    # Виведення книг по автору
    print("\nПублікації Ліна Костенко:")
    for pub in lib.books_by_author("Ліна Костенко"):
        print(pub.info())

    # Видалення книги та збереження у файлі
    with LibraryFileManager(lib, "library.json") as library:
        library.remove_book("Мистецтво війни")
        print("\nСписок публікацій після видалення книги:")
        for pub in library:
            print(pub.info())
            
    # Виведення всіх публікацій
    print("\nСписок всіх публікацій:")
    for pub in lib:
        print(pub.info())

    # Додавання книги «Мистецтво війни» назад
    book_04 = Book(BookModel(title="Мистецтво війни", author="Сунь-Цзи", year=500, type="book"))
    lib.add_book(book_04)
    lib.save_to_file("library.json")

    # Завантаження з файлу
    with LibraryFileManager(lib, "library.json") as loaded_library:
        print("\nСписок публікацій після завантаження з файлу:")
        for pub in loaded_library:
            print(pub.info())
