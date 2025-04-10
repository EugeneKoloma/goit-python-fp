import pickle
import sys
from contextlib import contextmanager

from contacts import ContactsBook
from output import output_error


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        output_error(
            f"File {filename} not found. New book was created, please proceed. All changes would be saved."
        )
        return ContactsBook()


@contextmanager
def book_cxt_mngr():
    try:
        book = load_data()
        yield book
    except Exception as error:
        raise error
    finally:
        save_data(book)
        sys.exit(0)
