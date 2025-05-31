from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Iterator, Literal
import json


# --- Decorators ---
def log_item_addition(func):
    def wrapper(self, item: PrintableItem, *args, **kwargs):
        print(f"[ITEM_ADDITION]: '{item.title}', {item.item_type}")
        return func(self, item, *args, **kwargs)
    return wrapper


def check_item_exists_before_removal(func):
    def wrapper(self, item_to_remove: PrintableItem, *args, **kwargs):
        if item_to_remove in self._items:
            print(f"[ITEM_REMOVAL] Елемент {item_to_remove.title} існує. Спроба видалення...")
            return func(self, item_to_remove, *args, **kwargs)
        else:
            print(f"[ITEM_REMOVAL_ERROR] Елемент {item_to_remove.title} не знайдено в бібліотеці.")
            return None
    return wrapper


def check_item_exists_before_addition(func):
    def wrapper(self, item: PrintableItem, *args, **kwargs):
        item_identity = f"'{item.title}'"

        if isinstance(item, Book):
            item_identity += f" (Автор: {item.author})"
        elif isinstance(item, Magazine):
            item_identity += f" (Випуск: {item.issue_number})"

        if item in self._items:
            print(f"[ITEM_ADDITION_ERROR] {item.item_type} {item_identity} вже є в бібліотеці.")
            return None
        else:
            return func(self, item, *args, **kwargs)
    return wrapper


def check_item_has_correct_type(func):
    def wrapper(self, item: PrintableItem, *args, **kwargs):
        if not isinstance(item, PrintableItem):
            print(
                f"[ITEM_ADDITION_ERROR] Об'єкт даного типу ({type(item)}) неможливо додати до бібліотеки. "
                f"Дозволені лише нащадки PrintableItem."
            )
            return None
        else:
            return func(self, item, *args, **kwargs)
    return wrapper


# --- Pydantic Models ---
class BookModel(BaseModel):
    item_type: Literal["book"]
    title: str
    author: str
    year: int


class MagazineModel(BaseModel):
    item_type: Literal["magazine"]
    title: str
    year: int
    issue_number: int


# --- Abstract Base Class ---
class PrintableItem(ABC):
    @property
    @abstractmethod
    def item_type(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def year(self) -> int:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict: # Словник для серіалізації в JSON
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


# --- Classes ---
class Book(PrintableItem):
    @property
    def item_type(self) -> str:
        return self.__item_data.item_type

    @property
    def title(self) -> str:
        return self.__item_data.title

    @property
    def author(self) -> str:
        return self.__item_data.author

    @property
    def year(self) -> int:
        return self.__item_data.year

    def __init__(self, book: BookModel):
        if not isinstance(book, BookModel):
            raise ValueError("book_data має бути екземпляром BookModel")
        self.__item_data = book

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title == other.title and
                self.author == other.author and
                self.year == other.year)

    def __hash__(self) -> int:
        return hash((self.item_type, self.title, self.author, self.year))

    def __repr__(self) -> str:
        return f"Book(title='{self.title}', author='{self.author}', year={self.year})"

    def get_info(self) -> str:
        return (f"Тип: {self.item_type}\n"
                f"Назва: {self.title}\n"
                f"Автор: {self.author}\n"
                f"Рік видання: {self.year}")

    def to_dict(self) -> dict:
        return {
            "item_type": self.item_type,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }


class Magazine(PrintableItem):
    @property
    def item_type(self) -> str:
        return self.__item_data.item_type

    @property
    def title(self) -> str:
        return self.__item_data.title

    @property
    def year(self) -> int:
        return self.__item_data.year

    @property
    def issue_number(self) -> int:
        return self.__item_data.issue_number

    def __init__(self, magazine: MagazineModel):
        if not isinstance(magazine, MagazineModel):
            raise ValueError("magazine має бути екземпляром MagazineModel")
        self.__item_data = magazine

    def __eq__(self, other) -> bool:
        if not isinstance(other, Magazine):
            return NotImplemented
        return (self.title == other.title and
                self.year == other.year and
                self.issue_number == other.issue_number)

    def __hash__(self) -> int:
        return hash((self.item_type, self.title, self.year, self.issue_number))

    def __repr__(self) -> str:
        return f"Magazine(title='{self.title}', year={self.year}, issue={self.issue_number})"

    def get_info(self) -> str:
        return (f"Тип: {self.item_type}\n"
                f"Назва: {self.title}\n"
                f"Рік видання: {self.year}\n"
                f"Номер випуску: {self.issue_number}")

    def to_dict(self) -> dict:
        return {
            "item_type": self.item_type,
            "title": self.title,
            "year": self.year,
            "issue_number": self.issue_number
        }


class Library:
    def __init__(self, items: List[PrintableItem] = None):
        if items is None:
            self._items: List[PrintableItem] = []
        else:
            self._items: List[PrintableItem] = [
                item for item in items if isinstance(item, PrintableItem)
            ]
            if len(self._items) != len(items if items else []):
                print("[LIBRARY_INIT_WARNING] Деякі елементи не були додані під час ініціалізації, оскільки не є екземплярами PrintableItem.")

    def __iter__(self) -> Iterator[PrintableItem]:
        return iter(self._items)

    def __str__(self) -> str:
        if not self._items:
            return "Бібліотека порожня."

        num_books = sum(1 for item in self._items if isinstance(item, Book))
        num_magazines = sum(1 for item in self._items if isinstance(item, Magazine))
        total_items = len(self._items)

        return (f"Елементи в бібліотеці: ({total_items} шт.)\n"
                f"  Книги: {num_books}\n"
                f"  Журнали: {num_magazines}")

    def get_books_by_author(self, author_name: str) -> Iterator[Book]:
        found_any = False
        for item in self._items:
            if isinstance(item, Book) and item.author == author_name:
                yield item
                found_any = True
        if not found_any:
            print(f"Книг автора '{author_name}' не знайдено.")

    def get_magazines_by_year(self, year: int) -> Iterator[Magazine]:
        found_any = False
        for item in self._items:
            if isinstance(item, Magazine) and item.year == year:
                yield item
                found_any = True
        if not found_any:
            print(f"Журналів за {year} рік не знайдено.")

    def get_items_by_title(self, title: str) -> Iterator[PrintableItem]:
        found_any = False
        for item in self._items:
            if item.title == title:
                yield item
                found_any = True
        if not found_any:
            print(f"Елементів з назвою '{title}' не знайдено.")

    @check_item_has_correct_type
    @check_item_exists_before_addition
    @log_item_addition
    def add_item(self, item: PrintableItem):
        self._items.append(item)

    @check_item_exists_before_removal
    def remove_item(self, item_to_remove: PrintableItem):
        self._items.remove(item_to_remove)

        item_type_str = item_to_remove.item_type
        details = f"'{item_to_remove.title}'"
        if isinstance(item_to_remove, Book):
            item_type_str = "Книгу"
            details += f" (Автор: {item_to_remove.author})"
        elif isinstance(item_to_remove, Magazine):
            item_type_str = "Журнал"
            details += f" (Випуск: {item_to_remove.issue_number})"
        print(f"{item_type_str} {details} видалено з бібліотеки.")

    def get_items(self) -> List[PrintableItem]:
        return self._items[:]

    def import_from_file(self, path: str):
        with FileOpener(path, 'r') as file:
            try:
                for line_number, line in enumerate(file, 1):
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue  # Пропустити порожні рядки
                    try:
                        data = json.loads(stripped_line)
                        json_item_type = data.get("item_type")

                        if json_item_type == "magazine":
                            model = MagazineModel(**data)
                            item_instance = Magazine(model)
                        elif json_item_type == "book":
                            model = BookModel(**data)
                            item_instance = Book(model)
                        else:
                            print(
                                f"[IMPORT_ERROR] Невідомий 'item_type': '{json_item_type}' в рядку: {stripped_line}")
                            continue

                        if item_instance:
                            self.add_item(item_instance)

                    except json.JSONDecodeError:
                        print(f"[IMPORT_ERROR] Неправильний формат JSON в рядку: {stripped_line}")
                    except Exception as e:
                        print(
                            f"[IMPORT_ERROR] Помилка при обробці елемента з рядка '{stripped_line}': {e}")
            except Exception as e:
                print(f"[IMPORT_ERROR] Помилка при читанні файлу '{path}': {e}")

    def export_to_file(self, path: str):
        with FileOpener(path, 'w') as file:
            try:
                for item in self._items:
                    item_dict = item.to_dict()
                    json_line = json.dumps(item_dict, ensure_ascii=False)
                    file.write(json_line + '\n')
                print(f"[EXPORT_SUCCESS] Дані успішно експортовано до файлу '{path}'.")
            except Exception as e:
                print(f"[EXPORT_ERROR] Помилка при експорті елементів до файлу '{path}': {e}")


class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
