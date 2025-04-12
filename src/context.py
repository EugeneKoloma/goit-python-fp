import pickle
from collections import namedtuple
from contextlib import contextmanager

from contacts import ContactsBook
from notes import Notes
from output import output_error


def save_data(data, filename=""):
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data(filename=""):
    if not filename:
        raise ValueError("Filename cannot be empty")
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except EOFError:
        output_error(
            f"File {filename} is empty. New book was created, please proceed. All changes would be saved."
        )
        return None
    except FileNotFoundError:
        output_error(
            f"File {filename} not found. New book was created, please proceed. All changes would be saved."
        )
        return None


@contextmanager
def data_cxt_mngr():
    book = None
    notes = None
    loaded_data = namedtuple("LoadedData", ["book", "notes"])
    try:
        book = load_data("contacts_book.pkl") or ContactsBook()
        notes = load_data("notes_book.pkl") or Notes()
        yield loaded_data(book, notes)
    except Exception as error:
        print(f"An error occurred: {error}")
        raise
    finally:
        if book is not None:
            save_data(book, "contacts_book.pkl")
        if notes is not None:
            save_data(notes, "notes_book.pkl")
