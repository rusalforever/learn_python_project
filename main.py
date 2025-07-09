import logging

from library import Library
from models import BookModel, MagazineModel

if __name__ == '__main__':
    try:

        library = Library()
        library.add_item(BookModel(title="1984", author="George Orwell", year=1949, type='book'))
        library.add_item(BookModel(title="Animal farm", author="George Orwell", year=1945, type='book'))
        library.add_item(BookModel(title="Brave New World", author="Aldous Huxley", year=1932, type='book'))
        library.add_item(MagazineModel(title="Sports Illustrated", author="Alex Author", year=1932, issue=2, month="January", type='magazine'))

        books = library.books
        print(books)

        gen = library.get_books_by_author("George Orwell")

        for book in gen:
            print(f'Using our generator: {book}')

        with library.file_manager('data/items.json', 'w') as lib:
            print(f"Saving {len(lib.books)} items to file")

        book_to_remove = next(
            (b for b in library.get_books_by_author("George Orwell") if b.title == "1984"),
            None
        )

        if book_to_remove:
            library.remove_item(book_to_remove)
            print("\nBook removed successfully.")
        else:
            print("\nBook not found.")

        print("\nUpdated book list:")
        print(library.books)

        with library.file_manager('data/items.json', 'r') as loaded_lib:
            for item in loaded_lib.all_library_items():
                already_exists = any(
                    i.title == item.title and i.author == item.author and i.year == item.year
                    for i in library.all_library_items()
                )
                if not already_exists:
                    print(f"\t{item.title}: {item.author} {item.typ} ({item.year})")
                    library.add_item(BookModel(title=item.title, author=item.author, year=item.year, type=item.type))
                    print(f"Added new item: {item.title} by {item.author}")
                else:
                    print(f"Skipped duplicate: {item.title} by {item.author}")


        logging.info("Reading library...")
        books = library.books
        print(books)


    except Exception as error:
        print(error)
