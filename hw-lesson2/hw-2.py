from classes import BookModel, Book, MagazineModel, Magazine, Library, PrintableItem

# Examples
if __name__ == '__main__':
    # --- Створення екземплярів BookModel та Book ---
    book_model1 = BookModel(item_type="book", title="Код да Вінчі", author="Ден Браун", year=2003)
    book1 = Book(book_model1)

    book_model2 = BookModel(item_type="book", title="1984", author="Джордж Орвелл", year=1949)
    book2 = Book(book_model2)

    book_model3 = BookModel(item_type="book", title="Гаррі Поттер і філософський камінь", author="Дж. К. Роулінг", year=1997)
    book3 = Book(book_model3)

    book_model4 = BookModel(item_type="book", title="Інферно", author="Ден Браун", year=2013)
    book4 = Book(book_model4)

    book_model5 = BookModel(item_type="book", title="Колгосп тварин", author="Джордж Орвелл", year=1945)
    book5 = Book(book_model5)

    # --- Створення екземплярів MagazineModel та Magazine ---
    magazine_model1 = MagazineModel(item_type="magazine", title="National Geographic", year=2023, issue_number=10)
    magazine1 = Magazine(magazine_model1)

    magazine_model2 = MagazineModel(item_type="magazine", title="Vogue", year=2023, issue_number=12)
    magazine2 = Magazine(magazine_model2)

    magazine_model3 = MagazineModel(item_type="magazine", title="National Geographic", year=2022, issue_number=5)
    magazine3 = Magazine(magazine_model3)


    data_file_path = 'library_data.jsonl'

    my_library = Library()
    print(my_library) # Порожня бібліотека
    print("-" * 40)

    # --- Демонстрація декораторів @check_item_exists_before_addition та @log_item_addition ---
    print("Демонстрація додавання елементів (книг та журналів):")
    my_library.add_item(book1)
    my_library.add_item(magazine1)
    my_library.add_item(book2)
    my_library.add_item(book4)
    my_library.add_item(magazine3)
    print(f"Поточний стан бібліотеки після початкового додавання:\n{my_library}")
    print("-" * 40)

    print("Спроба додати елемент, який вже існує (book1 - 'Код да Вінчі'):")
    my_library.add_item(book1) # Спроба додати дублікат книги
    print("Спроба додати елемент, який вже існує (magazine1 - 'National Geographic', 2023, випуск 10):")
    my_library.add_item(magazine1) # Спроба додати дублікат журналу
    print(f"Стан бібліотеки після спроби додати дублікати:\n{my_library}")
    # Перевірка, що кількість не змінилась (3 книги + 2 журнали = 5 елементів)
    assert len(my_library.get_items()) == 5
    print("-" * 40)

    print("Спроба додати не PrintableItem об'єкт:")
    my_library.add_item("Це не книга і не журнал") # Тестуємо додавання неправильного типу
    print(f"Стан бібліотеки:\n{my_library}")
    print("-" * 40)

    # --- Демонстрація декоратора check_item_exists_before_removal ---
    print("Демонстрація видалення елементів (з перевіркою наявності):")

    # 1. Видалення існуючої книги
    print("\nВидалення існуючої книги (book2 - '1984'):")
    book_to_remove_existing_data = BookModel(item_type="book", title="1984", author="Джордж Орвелл", year=1949)
    book_to_remove_existing = Book(book_to_remove_existing_data)
    my_library.remove_item(book_to_remove_existing)
    print(f"Стан бібліотеки після видалення '1984':\n{my_library}")
    print("-" * 40)

    # 2. Видалення існуючого журналу
    print("\nВидалення існуючого журналу (magazine3 - 'National Geographic', 2022, випуск 5):")
    magazine_to_remove_existing_data = MagazineModel(item_type="magazine", title="National Geographic", year=2022, issue_number=5)
    magazine_to_remove_existing = Magazine(magazine_to_remove_existing_data)
    my_library.remove_item(magazine_to_remove_existing)
    print(f"Стан бібліотеки після видалення журналу 'National Geographic' (2022):\n{my_library}")
    print("-" * 40)

    # 3. Спроба видалити елемент, якого немає в бібліотеці (книга)
    print("\nСпроба видалити неіснуючу книгу (book3 - 'Гаррі Поттер'):")
    my_library.remove_item(book3) # book3 не додавали до my_library, або вже видалили
    print(f"Стан бібліотеки (має бути без змін):\n{my_library}")
    print("-" * 40)

    # 4. Спроба видалити елемент, який щойно був видалений (book2 - '1984')
    print("\nСпроба повторно видалити книгу '1984':")
    my_library.remove_item(book_to_remove_existing) # Вже видалена
    print(f"Стан бібліотеки (має бути без змін):\n{my_library}")
    print("-" * 40)


    # --- Демонстрація ітератора та генераторів ---
    print("Додамо ще кілька елементів для демонстрації ітератора/генераторів:")
    my_library.add_item(book5)      # 'Колгосп тварин'
    my_library.add_item(book3)      # 'Гаррі Поттер'
    my_library.add_item(magazine2)  # 'Vogue'
    # На цей момент my_library містить: book1, book4, magazine1, book5, book3, magazine2
    print(f"Поточний стан бібліотеки:\n{my_library}")
    print("-" * 40)

    print("Використання ітератора (for item in my_library):")
    print("Книги:")
    for item in my_library:
        if isinstance(item, Book):
            print(f"  - '{item.title}' by {item.author} ({item.year})")
        else:
            continue

    print("Журнали:")
    for item in my_library:
        if isinstance(item, Magazine):
            print(f"  - '{item.title}', рік: {item.year}, випуск: {item.issue_number}")
        else:
            continue
    print("-" * 40)

    print("Використання генератора get_books_by_author:")
    print("\nКниги Дена Брауна:")
    for book_by_author in my_library.get_books_by_author("Ден Браун"):
        print(f"  Знайдено: {book_by_author.title}")

    print("\nКниги Джорджа Орвелла:")
    for book_by_author in my_library.get_books_by_author("Джордж Орвелл"):
        print(f"  Знайдено: {book_by_author.title}")
    print("-" * 40)

    print("Використання генератора get_magazines_by_year:")
    print("\nЖурнали за 2023 рік:")
    for mag_by_year in my_library.get_magazines_by_year(2023):
        print(f"  Знайдено: {mag_by_year.title}, випуск: {mag_by_year.issue_number}")

    print("\nЖурнали за 2021 рік (немає):")
    for mag_by_year in my_library.get_magazines_by_year(2021):
        print(f"  Знайдено: {mag_by_year.title}, випуск: {mag_by_year.issue_number}")
    print("-" * 40)

    print("Використання генератора get_items_by_title:")
    print("\nЕлементи з назвою 'National Geographic':")
    for item_by_title in my_library.get_items_by_title("National Geographic"):
        if isinstance(item_by_title, Magazine):
            print(f"  Знайдено журнал: {item_by_title.title}, рік: {item_by_title.year}, випуск: {item_by_title.issue_number}")
        else:
            print(f"  Знайдено: {item_by_title.title} ({item_by_title.item_type})")

    print("\nЕлементи з назвою 'Неіснуюча Назва':")
    for item_by_title in my_library.get_items_by_title("Неіснуюча Назва"): # Цей цикл не виконається
        print(f"  Знайдено: {item_by_title.title}")
    print("-" * 40)


    # --- Демонстрація експорту та імпорту файлів ---
    print("Демонстрація експорту та імпорту файлів:")
    # На цей момент my_library містить: book1, magazine1, book4, book5, book3, magazine2 (6 елементів)
    current_items_in_my_library_before_export = list(my_library)
    print(f"\n1. Експорт елементів з 'my_library' (містить {len(current_items_in_my_library_before_export)} елементи):")
    print("Елементи для експорту:")
    for item in my_library:
        print(f"  - '{item.title}' ({item.item_type})")
    my_library.export_to_file(data_file_path)
    print(f"Елементи експортовано у файл '{data_file_path}'.")
    print("-" * 40)


    # 2. Імпорт у нову порожню бібліотеку
    print("\n2. Імпорт елементів у нову бібліотеку ('imported_library'):")
    imported_library = Library()
    print(f"Стан 'imported_library' перед імпортом:\n{imported_library}")
    imported_library.import_from_file(data_file_path)
    print(
        f"\nСтан 'imported_library' після імпорту:\n{imported_library} (містить {len(imported_library.get_items())} елементи)")
    print("Елементи в 'imported_library':")
    if not imported_library.get_items():
        print("  Імпортована бібліотека порожня.")
    else:
        for item in imported_library:
            if isinstance(item, Book):
                print(f"  - Книга: '{item.title}' by {item.author}")
            elif isinstance(item, Magazine):
                print(f"  - Журнал: '{item.title}', рік: {item.year}, випуск: {item.issue_number}")
    assert len(imported_library.get_items()) == len(current_items_in_my_library_before_export)
    print("-" * 40)


    # 3. Повторний імпорт у 'my_library' (дублікати будуть пропущені декоратором)
    print("\n3. Повторний імпорт у 'my_library' (дублікати будуть пропущені):")
    initial_item_count_my_library = len(my_library.get_items())
    print(f"Кількість елементів у 'my_library' перед повторним імпортом: {initial_item_count_my_library}")

    my_library.import_from_file(data_file_path)
    print(f"\nСтан 'my_library' після повторного імпорту:\n{my_library} (містить {len(my_library.get_items())} елементів)")
    print(f"Очікувана кількість елементів: {initial_item_count_my_library} (не змінилася, бо дублікати пропущено)")

    assert len(my_library.get_items()) == initial_item_count_my_library
    print("-" * 40)


    # 4. Демонстрація імпорту з файлу з помилками та частковим успіхом
    print("\n4. Демонстрація імпорту з файлу, що містить помилки та дублікати:")
    print(f"Створення файлу '{data_file_path}' з некоректними даними...")

    # У файлі буде:
    # 1. Коректна книга 1 (унікальна)
    # 2. Коректний журнал 1 (унікальний)
    # 3. Рядок, що не є JSON
    # 4. Книга з помилкою валідації Pydantic (рік - не число)
    # 5. Журнал з помилкою валідації Pydantic (відсутній номер випуску)
    # 6. Коректна книга 2 (унікальна)
    # 7. Порожній JSON {} (спричинить помилку Pydantic)
    # 8. JSON з невідомим item_type
    # 9. Коректний журнал 2 (унікальний)
    # 10. Дублікат книги 1 (буде пропущено)
    # 11. Дублікат журналу 1 (буде пропущено)
    # Очікується імпорт: Книга 1, Журнал 1, Книга 2, Журнал 2 (всього 4 елементи)
    with open(data_file_path, 'w', encoding='utf-8') as f:
        f.write('{"item_type": "book", "title": "Унікальна Книга Імпорт 1", "author": "Автор Тест Імпорт", "year": 2020}\n')
        f.write('{"item_type": "magazine", "title": "Унікальний Журнал Імпорт 1", "year": 2021, "issue_number": 1}\n')
        f.write('Це не JSON рядок.\n')
        f.write('{"item_type": "book", "title": "Книга з помилкою року", "author": "Автор Тест Помилка", "year": "не_число"}\n')
        f.write('{"item_type": "magazine", "title": "Журнал без номера", "year": 2022}\n') # Відсутній issue_number
        f.write('{"item_type": "book", "title": "Унікальна Книга Імпорт 2", "author": "Автор Тест Імпорт", "year": 2022}\n')
        f.write('{}\n')
        f.write('{"item_type": "newspaper", "title": "Газета", "year": 2023}\n') # Невідомий item_type
        f.write('{"item_type": "magazine", "title": "Унікальний Журнал Імпорт 2", "year": 2023, "issue_number": 2}\n')
        f.write('{"item_type": "book", "title": "Унікальна Книга Імпорт 1", "author": "Автор Тест Імпорт", "year": 2020}\n') # Дублікат
        f.write('{"item_type": "magazine", "title": "Унікальний Журнал Імпорт 1", "year": 2021, "issue_number": 1}\n') # Дублікат

    error_test_library = Library()
    print(f"Стан 'error_test_library' перед імпортом з помилками:\n{error_test_library}")
    print(f"\nРозпочинаємо імпорт з файлу '{data_file_path}', що містить помилки та дублікат:")
    error_test_library.import_from_file(data_file_path)

    print(
        f"\nСтан 'error_test_library' після імпорту:\n{error_test_library} (містить {len(error_test_library.get_items())} елементи)")
    print("Елементи, які вдалося імпортувати в 'error_test_library':")
    imported_count = 0
    if not error_test_library.get_items():
        print("  Жодного елемента не було імпортовано.")
    else:
        for item in error_test_library:
            if isinstance(item, Book):
                print(f"  - Книга: '{item.title}' by {item.author}, рік: {item.year}")
            elif isinstance(item, Magazine):
                print(f"  - Журнал: '{item.title}', рік: {item.year}, випуск: {item.issue_number}")
            imported_count +=1
    print(f"(Всього імпортовано коректних та унікальних: {imported_count} елементи)")
    assert imported_count == 4 # Очікуємо 4 унікальні коректні елементи
    print("-" * 40)

    # Відновлення файлу data_file_path з поточним станом 'my_library'
    print(f"\nВідновлення файлу '{data_file_path}' з поточним станом 'my_library' ({len(my_library.get_items())} елементів):")
    my_library.export_to_file(data_file_path)
    print(f"Файл '{data_file_path}' оновлено.")
    print("Демонстрацію завершено.")
    print("-" * 40)
