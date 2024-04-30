import argparse

# Клас для книги
class BookModel:
    def __init__(self, title: str, author: str, year: int, genre: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

# Клас для журналу
class JournalModel:
    def __init__(self, title: str, author: str, date: str, type: str):
        self.title = title
        self.author = author
        self.date = date
        self.type = type

# Клас для бібліотеки книг та журналів
class Library:
    def __init__(self):
        self.items = []

    # Метод додавання книги або журналу
    def add_item(self, item):
        self.items.append(item)
        if isinstance(item, BookModel):
            print(f"До бібліотеки додано книгу: {item.title}")
        elif isinstance(item, JournalModel):
            print(f"До бібліотеки додано журнал: {item.title}")

    # Метод видалення книги або журналу
    def remove_item(self, title: str):
        for item in self.items:
            if item.title == title:
                self.items.remove(item)
                print(f"З бібліотеки видалено елемент: {title}")
                return
        print(f"Елемент '{title}' відсутній в бібліотеці")

    # Метод для виведення списку книг та журналів
    def list_items(self):
        if not self.items:
            print("У бібліотеці немає жодних книг або журналів")
        else:
            print("Список книг та журналів у бібліотеці:")
            for item in self.items:
                if isinstance(item, BookModel):
                    print(f"Книга: Назва: {item.title}, Автор: {item.author}, Рік: {item.year}, Жанр: {item.genre}")
                elif isinstance(item, JournalModel):
                    print(f"Журнал: Назва: {item.title}, Автор: {item.author}, Дата: {item.date}, Тип: {item.type}")

    # Метод для збереження списку книг та журналів у файл
    def save_items_to_file(self, filename):
        with open(filename, 'w') as file:
            for item in self.items:
                if isinstance(item, BookModel):
                    file.write(f"Book,{item.title},{item.author},{item.year},{item.genre}\n")
                elif isinstance(item, JournalModel):
                    file.write(f"Journal,{item.title},{item.author},{item.date},{item.type}\n")

    # Метод для завантаження списку книг та журналів з файлу
    def load_items_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                type, *data = line.strip().split(',')
                if type == 'Book':
                    title, author, year, genre = data
                    book = BookModel(title, author, int(year), genre)
                    self.add_item(book)
                elif type == 'Journal':
                    title, author, date, type = data
                    journal = JournalModel(title, author, date, type)
                    self.add_item(journal)


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Додати книгу")
        print("2. Додати журнал")
        print("3. Видалити елемент")
        print("4. Вивести список книг та журналів у бібліотеці")
        print("5. Зберегти список книг та журналів у файл")
        print("6. Завантажити список книг та журналів з файлу")
        print("7. Вийти з програми")

        choice = input("Оберіть операцію: ")

        if choice == '1':
            title = input("Введіть назву книги: ")
            author = input("Введіть автора книги: ")
            year = int(input("Введіть рік видання книги: "))
            genre = input("Введіть жанр книги: ")
            book = BookModel(title, author, year, genre)
            library.add_item(book)
        elif choice == '2':
            title = input("Введіть назву журналу: ")
            author = input("Введіть автора журналу: ")
            date = input("Введіть дату видання журналу: ")
            type = input("Введіть тип журналу (ранковий, вечірній, тижневий): ")
            journal = JournalModel(title, author, date, type)
            library.add_item(journal)
        elif choice == '3':
            title = input("Введіть назву елемента для видалення: ")
            library.remove_item(title)
        elif choice == '4':
            library.list_items()
        elif choice == '5':
            filename = input("Введіть назву файлу для збереження книг та журналів: ")
            library.save_items_to_file(filename)
        elif choice == '6':
            filename = input("Введіть назву файлу для завантаження книг та журналів: ")
            library.load_items_from_file(filename)
        elif choice == '7':
            print("Програма завершена.")
            break
        else:
            print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
