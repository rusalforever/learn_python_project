from classes import BookModel, Book, Library


# Examples
if __name__ == '__main__':
    # Створення екземплярів BookModel та Book
    book_model1 = BookModel(title="Код да Вінчі", author="Ден Браун", year=2003)
    book1 = Book(book_model1)

    book_model2 = BookModel(title="1984", author="Джордж Орвелл", year=1949)
    book2 = Book(book_model2)

    book_model3 = BookModel(title="Гаррі Поттер і філософський камінь", author="Дж. К. Роулінг", year=1997)
    book3 = Book(book_model3)

    book_model4 = BookModel(title="Інферно", author="Ден Браун", year=2013)
    book4 = Book(book_model4)

    book_model5 = BookModel(title="Колгосп тварин", author="Джордж Орвелл", year=1945)
    book5 = Book(book_model5)

    # Ім'я файлу для операцій експорту/імпорту
    data_file_path = 'library_data.txt'

    # Створення бібліотеки
    my_library = Library()
    print(my_library) # Порожня бібліотека
    print("-" * 40)

    # --- Демонстрація декораторів @check_book_exists_before_addition та @log_book_addition ---
    print("Демонстрація додавання книг:")
    my_library.add_book(book1) # Успішне додавання
    my_library.add_book(book2) # Успішне додавання
    my_library.add_book(book4) # Успішне додавання
    print(f"Поточний стан бібліотеки після початкового додавання: {my_library}")
    print("-" * 40)

    print("Спроба додати книгу, яка вже існує (book1 - 'Код да Вінчі'):")
    my_library.add_book(book1) # Спроба додати дублікат
    print(f"Стан бібліотеки після спроби додати дублікат: {my_library} (кількість книг не має змінитися)")
    assert len(my_library.get_books()) == 3 # Перевірка, що кількість не змінилась
    print("-" * 40)

    print("Спроба додати не Book об'єкт:")
    my_library.add_book("Це не книга") # Тестуємо додавання неправильного типу
    print(f"Стан бібліотеки: {my_library}")
    print("-" * 40)

    # --- Демонстрація декоратора check_book_exists_before_removal ---
    print("Демонстрація видалення книг (з перевіркою наявності):")

    # 1. Видалення існуючої книги
    print("\nВидалення існуючої книги (book2 - '1984'):")
    # Створюємо новий екземпляр Book для видалення, щоб перевірити роботу __eq__
    book_to_remove_existing_data = BookModel(title="1984", author="Джордж Орвелл", year=1949)
    book_to_remove_existing = Book(book_to_remove_existing_data)
    my_library.remove_book(book_to_remove_existing)
    print(f"Стан бібліотеки після видалення '1984': {my_library}")
    print("-" * 40)

    # 2. Спроба видалити книгу, якої немає в бібліотеці
    print("\nСпроба видалити неіснуючу книгу (book3 - 'Гаррі Поттер'):")
    my_library.remove_book(book3) # book3 не додавали до my_library, або вже видалили
    print(f"Стан бібліотеки (має бути без змін): {my_library}")
    print("-" * 40)

    # 3. Спроба видалити книгу, яка щойно була видалена (book2 - '1984')
    print("\nСпроба повторно видалити книгу '1984':")
    my_library.remove_book(book_to_remove_existing) # Вже видалена
    print(f"Стан бібліотеки (має бути без змін): {my_library}")
    print("-" * 40)


    # --- Демонстрація ітератора та генератора ---
    print("Додамо ще кілька книг для демонстрації ітератора/генератора:")
    my_library.add_book(book5) # 'Колгосп тварин'
    my_library.add_book(book3) # 'Гаррі Поттер'
    # На цей момент my_library містить: book1, book4, book5, book3
    print(f"Поточний стан бібліотеки: {my_library}")
    print("-" * 40)

    print("Використання ітератора (for book in my_library):")
    for book_item in my_library:
        print(f"  - {book_item.name} by {book_item.author} ({book_item.year})")
    print("-" * 40)

    print("Використання генератора (get_books_by_author):")
    print("\nКниги Дена Брауна:")
    found_db_books = False
    for book_by_author in my_library.get_books_by_author("Ден Браун"):
        print(f"  Знайдено: {book_by_author.name}")
        found_db_books = True
    if not found_db_books:
         print("  Книг Дена Брауна не знайдено.")

    print("\nКниги Джорджа Орвелла:")
    found_go_books = False
    for book_by_author in my_library.get_books_by_author("Джордж Орвелл"):
        print(f"  Знайдено: {book_by_author.name}")
        found_go_books = True
    if not found_go_books:
        print("  Книг Джорджа Орвелла не знайдено.")

    print("\nСпроба знайти книги неіснуючого автора:")
    found_na_books = False
    for book_by_author in my_library.get_books_by_author("Неіснуючий Автор"):
        print(f"  Знайдено: {book_by_author.name}")
        found_na_books = True
    print("-" * 40)


    # --- Демонстрація експорту та імпорту файлів ---
    print("Демонстрація експорту та імпорту файлів:")

    # 1. Експорт поточної бібліотеки 'my_library'
    # На цей момент my_library містить: book1, book4, book5, book3 (4 книги)
    current_books_in_my_library_before_export = list(my_library)
    print(f"\n1. Експорт книг з 'my_library' (містить {len(current_books_in_my_library_before_export)} книги):")
    print("Книги для експорту:")
    for book_item in my_library:
        print(f"  - '{book_item.name}'")
    my_library.export_to_file(data_file_path)
    print(f"Книги експортовано у файл '{data_file_path}'.")
    print("-" * 40)


    # 2. Імпорт у нову порожню бібліотеку
    print("\n2. Імпорт книг у нову бібліотеку ('imported_library'):")
    imported_library = Library()
    print(f"Стан 'imported_library' перед імпортом: {imported_library}")
    imported_library.import_from_file(data_file_path)
    print(
        f"\nСтан 'imported_library' після імпорту: {imported_library} (містить {len(imported_library.get_books())} книги)")
    print("Книги в 'imported_library':")
    if not imported_library.get_books():
        print("  Імпортована бібліотека порожня.")
    else:
        for book_item in imported_library:
            print(f"  - '{book_item.name}' by {book_item.author}")
    assert len(imported_library.get_books()) == len(current_books_in_my_library_before_export)
    print("-" * 40)


    # 3. Повторний імпорт у 'my_library' (дублікати будуть пропущені декоратором)
    print("\n3. Повторний імпорт у 'my_library' (дублікати будуть пропущені):")
    initial_book_count_my_library = len(my_library.get_books())
    print(f"Кількість книг у 'my_library' перед повторним імпортом: {initial_book_count_my_library}")

    my_library.import_from_file(data_file_path)
    print(f"\nСтан 'my_library' після повторного імпорту: {my_library} (містить {len(my_library.get_books())} книг)")
    print(f"Очікувана кількість книг: {initial_book_count_my_library} (не змінилася, бо дублікати пропущено)")

    assert len(my_library.get_books()) == initial_book_count_my_library # Перевірка, що кількість не змінилась
    print("-" * 40)


    # 4. Демонстрація імпорту з файлу з помилками та частковим успіхом (включаючи дублікат)
    print("\n4. Демонстрація імпорту з файлу, що містить помилки та дублікати:")
    print(f"Створення файлу '{data_file_path}' з некоректними даними...")

    # У файлі буде 3 унікальні коректні книги, 1 дублікат і кілька помилкових рядків
    with open(data_file_path, 'w', encoding='utf-8') as f:
        f.write('{"title": "Нова Унікальна Книга 1", "author": "Автор Тест Імпорт", "year": 2020}\n')
        f.write('Це не JSON рядок.\n') # Помилка JSONDecodeError
        f.write('{"title": "Книга з помилкою року", "author": "Автор Тест Помилка", "year": "не_число"}\n') # Помилка Pydantic
        f.write('{"title": "Нова Унікальна Книга 2", "author": "Автор Тест Імпорт", "year": 2022}\n')
        f.write('{}\n') # Порожній JSON, спричинить помилку Pydantic (відсутні поля)
        f.write('{"title": "Книга без автора", "year": 2021}\n') # Помилка Pydantic (відсутнє поле author)
        f.write('{"title": "Нова Унікальна Книга 3", "author": "Автор Тест Імпорт", "year": 2023}\n')
        f.write('{"title": "Нова Унікальна Книга 1", "author": "Автор Тест Імпорт", "year": 2020}\n') # Дублікат, буде пропущено декоратором

    error_test_library = Library()
    print(f"Стан 'error_test_library' перед імпортом з помилками: {error_test_library}")
    print(f"\nРозпочинаємо імпорт з файлу '{data_file_path}', що містить помилки та дублікат:")
    error_test_library.import_from_file(data_file_path)

    print(
        f"\nСтан 'error_test_library' після імпорту: {error_test_library} (містить {len(error_test_library.get_books())} книги)")
    print("Книги, які вдалося імпортувати в 'error_test_library':")
    imported_count = 0
    if not error_test_library.get_books():
        print("  Жодної книги не було імпортовано.")
    else:
        for book_item in error_test_library:
            print(f"  - '{book_item.name}' by {book_item.author}, рік: {book_item.year}")
            imported_count +=1
    print(f"(Всього імпортовано коректних та унікальних: {imported_count} книги)")
    assert imported_count == 3 # Очікуємо 3 унікальні коректні книги
    print("-" * 40)

    # Відновлення файлу data_file_path з поточним станом 'my_library'
    # 'my_library' містить 4 книги, які були там до всіх маніпуляцій з файлом у п.4
    print(f"\nВідновлення файлу '{data_file_path}' з поточним станом 'my_library' ({len(my_library.get_books())} книг):")
    my_library.export_to_file(data_file_path) # Передаємо шлях до файлу
    print(f"Файл '{data_file_path}' оновлено.")
    print("Демонстрацію завершено.")
    print("-" * 40)