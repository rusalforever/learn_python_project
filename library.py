from pydantic import BaseModel
from abc import ABC, abstractmethod
from contextlib import contextmanager

class BookModel(BaseModel):
    name: str
    author: str
    year: int

class Book:
    def __init__(self, model: BookModel):
        self.__name = model.name
        self.author = model.author
        self.year = model.year

    def __str__(self):
        return f'Назва: {self.__name}, Автор: {self.author}, Рік видання: {self.year}'

    @staticmethod
    def from_txt_line(line: str):
        parts = line.strip().split(';')
        if len(parts) != 4:
            raise ValueError("Неправильний формат рядка")
        typ, name, author, year = parts
        year = int(year)
        if typ == "Book":
            return Book(BookModel(name=name, author=author, year=year))
        elif typ == "Magazine":
            return Magazine(BookModel(name=name, author=author, year=year))
        else:
            raise ValueError(f"Невідомий тип запису: {typ}")

    @property
    def name(self):
        return self.__name

    def to_txt_line(self) -> str:
        return f"Book;{self.name};{self.author};{self.year}"

class Magazine(Book):
    def __init__(self, model: BookModel):
        super().__init__(model)
        self.number = model.year

    def __str__(self):
        return f'Журнал: {self.name}, Редактор: {self.author}, Номер: {self.number}'

    def to_txt_line(self) -> str:
        return f"Magazine;{self.name};{self.author};{self.number}"

class LibraryBook:
    def __init__(self, items=None):
        self.items = items if items else []

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.items):
            raise StopIteration
        item = self.items[self.current_index]
        self.current_index += 1
        return item

    def item_generator(self):
        for item in self.items:
            yield item

    def via_for_loop(self):
        for item in self.item_generator():
            print(item)

    def items_by_author(self, author_name: str):
        for item in self.items:
            if item.author == author_name:
                yield item

    @staticmethod
    def log_addition(func):
        def wrapper(self, item, *args, **kwargs):
            print(f"Додавання: {item.name}, автор: {item.author}")
            return func(self, item, *args, **kwargs)
        return wrapper

    @staticmethod
    def check_exists(func):
        def wrapper(self, item, *args, **kwargs):
            if item not in self.items:
                print(f"'{item.name}' не знайдено в бібліотеці.")
                return
            return func(self, item, *args, **kwargs)
        return wrapper

    @log_addition
    def add_item(self, item):
        self.items.append(item)

    @check_exists
    def remove_item(self, item):
        self.items.remove(item)

    @staticmethod
    @contextmanager
    def open_library_file(filename: str, mode: str = 'w'):
        f = None
        try:
            f = open(filename, mode, encoding='utf-8')
            yield f
        finally:
            if f:
                f.close()

    def save_to_txt(self, filename):
        with LibraryBook.open_library_file(filename, 'w') as f:
            for item in self.items:
                f.write(item.to_txt_line() + '\n')
        print(f"Збережено у {filename}")

    def load_from_txt(self, filename: str):
        with LibraryBook.open_library_file(filename, 'r') as f:
            for line in f:
                try:
                    item = Book.from_txt_line(line)
                    self.add_item(item)
                except Exception as e:
                    print(f"Не вдалося завантажити рядок: {line.strip()} помилка: {e}")

class Workers(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def job_position(self):
        raise NotImplementedError

class Librarian(Workers):
    def __init__(self, name, pos: str = 'бібліотекар'):
        super().__init__(name)
        self.__job_position = pos

    @property
    def job_position(self):
        return self.__job_position

class Cleaner(Workers):
    def __init__(self, name, pos: str = 'прибиральник'):
        super().__init__(name)
        self.__job_position = pos

    @property
    def job_position(self):
        return self.__job_position

if __name__ == "__main__":
    worker1 = Librarian("Олена")
    worker2 = Cleaner("Петро")

    print(f"{worker1.name} працює як {worker1.job_position}")
    print(f"{worker2.name} працює як {worker2.job_position}")

    b1 = Book(BookModel(name="Кобзар", author="Т. Шевченко", year=1840))
    b2 = Book(BookModel(name="Фізика", author="І. Франко", year=1900))
    m1 = Magazine(BookModel(name="Наука і Життя", author="Ред. Іваненко", year=3))

    lib = LibraryBook()

    lib.add_item(b1)
    lib.add_item(b2)
    lib.add_item(m1)

    print("\n--- Всі записи ---")
    lib.via_for_loop()

    print("\n--- Книги автора І. Франко ---")
    for item in lib.items_by_author("І. Франко"):
        print(item)

    lib.save_to_txt("library.txt")

    lib.remove_item(b2)

    print("\n--- Після видалення ---")
    lib.via_for_loop()

    new_lib = LibraryBook()
    new_lib.load_from_txt("library.txt")

    print("\n--- Після завантаження з файлу ---")
    new_lib.via_for_loop()