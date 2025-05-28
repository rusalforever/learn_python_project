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

    # Створення бібліотеки
    my_library = Library()
    print(my_library) # Порожня бібліотека
    print("-" * 40)

    # --- Демонстрація декоратора log_book_addition ---
    print("Демонстрація додавання книг:")
    my_library.add_book(book1)
    my_library.add_book(book2)
    my_library.add_book(book4)
    print("-" * 40)

    print("Спроба додати не Book об'єкт:")
    my_library.add_book("Це не книга") # Тестуємо додавання неправильного типу
    print("-" * 40)
    print("Поточний стан бібліотеки:")
    print(my_library)
    print("-" * 40)

    # --- Демонстрація декоратора check_book_exists_before_removal ---
    print("Демонстрація видалення книг (з перевіркою наявності):")

    # 1. Видалення існуючої книги
    print("\nВидалення існуючої книги (book2 - '1984'):")
    book_to_remove_existing_data = BookModel(title="1984", author="Джордж Орвелл", year=1949)
    book_to_remove_existing = Book(book_to_remove_existing_data)
    my_library.remove_book(book_to_remove_existing)
    print("Стан бібліотеки після видалення '1984':")
    print(my_library)
    print("-" * 40)

    # 2. Спроба видалити книгу, якої немає в бібліотеці
    print("\nСпроба видалити неіснуючу книгу (book3 - 'Гаррі Поттер'):")
    my_library.remove_book(book3) # book3 не додавали, або вже видалили
    print("Стан бібліотеки (має бути без змін):")
    print(my_library)
    print("-" * 40)

    # 3. Спроба видалити книгу, яка щойно була видалена (book2 - '1984')
    print("\nСпроба повторно видалити книгу '1984':")
    my_library.remove_book(book_to_remove_existing) # Вже видалена
    print("Стан бібліотеки (має бути без змін):")
    print(my_library)
    print("-" * 40)

    # 4. Спроба видалити не Book об'єкт
    print("\nСпроба видалити не Book об'єкт:")
    my_library.remove_book(12345)
    print("Стан бібліотеки (має бути без змін):")
    print(my_library)
    print("-" * 40)

    # --- Демонстрація ітератора та генератора ---
    print("Додамо ще кілька книг для демонстрації ітератора/генератора:")
    my_library.add_book(book5) # 'Колгосп тварин'
    my_library.add_book(book3) # 'Гаррі Поттер'
    print(my_library)
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
        print(f"  Знайдено: {book_by_author.name}") # Цей рядок не виконається
        found_na_books = True
    if not found_na_books:
        print("  (Підтвердження: генератор не повернув жодної книги для 'Неіснуючий Автор')")
