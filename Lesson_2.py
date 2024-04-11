import json

from pydantic import BaseModel
from abc import ABC, abstractmethod


def logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'Add book or journal:     {result.item_info()}')
        return result
    return wrapper
def delet(func):
    def wrapper(*args, **kwargs):
        print('Trying to find a book or magazine to remove from this library list:')
        lib.show_library()
        result = func(*args, **kwargs)
        return result
    return wrapper

class BookModel(BaseModel):
    name: str
    author: str
    year: int

class JournalModel(BookModel):
    edition: int

class AbstractLibraryItem(ABC):
    @abstractmethod
    def item_info(self):
        raise NotImplementedError

class Book(AbstractLibraryItem):
    def __init__(self, model: BookModel):
        self.model = model
    def item_info(self):
        return {self.model.name:{'author':self.model.author, "year":self.model.year}}


class Journal(AbstractLibraryItem):
    def __init__(self, model: JournalModel):
        self.model = model

    def item_info(self):
        return {self.model.name:{'author':self.model.author, "year":self.model.year, "edition":self.model.edition}}



class Library:
    def __init__(self):
        self.item_list = []

    @logger
    def add_book(self, item: AbstractLibraryItem):
        self.item_list.append(item)
        return item


    def get_item_by_author(self, name:str):
        list_books_journal = []
        gener = (i for i in self.item_list)
        for book in gener:
            if book.model.author == name:
                list_books_journal.append(book.item_info())
        if list_books_journal:
            return print(list_books_journal)
        else:
            print(f'Нет книг автора {name} в списке!')


    def show_library(self):
        for book_and_journal in self.item_list:
            print(book_and_journal.item_info())

    def save_list_book_journal(self):
        try:
            with open('list_books_and_journal.json', 'w', encoding='utf-8') as file:
                for i in self.item_list:
                    file.write(str(i.item_info()) + '\n')
        except Exception as e:
            print(f'Error add: {e}')
    @delet
    def delete_book_or_journal(self, name:str):
        for item in self.item_list:
            if item.model.name == name:
                self.item_list.remove(item)
                print(f'Book of journal "{name}" has been removed from the library')
                break
        else:
            print(f'Book of journal "{name}" not in the library')
    #
    def show_list_books_after_deletion(self):
        self.item_list.clear()
        print('Library cleared')

    def add_books_is_file(self):
        try:
            with open('json_list.json', 'r', encoding='utf-8') as file_json:
                data = json.load(file_json)  # Загрузка всего файла как JSON массив
                for line in data:
                    if 'edition' in line:
                        journal_model = JournalModel(**line)
                        journal = Journal(journal_model)
                        self.add_book(journal)
                    else:
                        book_model = BookModel(**line)
                        book = Book(book_model)
                        self.add_book(book)
        except Exception as e:
            print(f'Error add: {e}')

journal_1 = {'name': 'Forbes',
          'author': 'Charlz',
          'year': 2005,
          'edition':88
}

book_1 = {'name': 'Mavka',
          'author': 'Ukrayinka',
          'year': 2020,
}
book_2 = {'name': 'Zapovit',
          'author': 'Shevchenko',
          'year': 2020,
}

book_3 = {'name': 'Kobzar',
          'author': 'Shevchenko',
          'year': 2021,
}

    if __name__ == '__main__':
        print('**** Add book or journal *****')
        lib = Library()
        journal_model = JournalModel(**journal_1)
        journal = Journal(journal_model)
        lib.add_book(journal)
        print()

        print('**** Add book or journal *****')
        book_model = BookModel(**book_1)
        book = Book(book_model)
        lib.add_book(book)
        print()

        print('**** Add book or journal *****')
        book_model = BookModel(**book_2)
        book = Book(book_model)
        lib.add_book(book)
        print()
        print()
        print('**** Add book or journal *****')
        book_model = BookModel(**book_3)
        book = Book(book_model)
        lib.add_book(book)
        print( '\t' * 3, ' **** Show entire library*****')
        lib.show_library()


        #
        print()
        print('**** Search for a book or journal by author *****')
        lib.get_item_by_author('Shevchenko') #input АВТОРА
        #
        print()
        print('**** Saving to file *****')
        lib.save_list_book_journal()
        #
        print()
        print('**** Removing a book from the library *****')
        lib.delete_book_or_journal('Mavka')
        #
        print()
        print('**** Displaying a list of books or journals after deletion *****')
        lib.show_library()
        #
        print()
        print('**** Clear entire library *****')
        lib.show_list_books_after_deletion()
        #
        print()
        print('**** Displaying a list of books of journals after deletion *****')
        lib.show_library()
        #
        print()
        print('**** Adding books of journals from a file *****')
        lib.add_books_is_file()

        print()
        print('**** Show entire library *****')
        lib.show_library()


