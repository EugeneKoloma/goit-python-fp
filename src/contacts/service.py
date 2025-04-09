from colorama import Fore

from decorators import error_handler
from exceptions import FieldNotFound, PhoneAlreadyOwned, RecordNotFound
from output import output_info, output_warning

from .ContactsBook import ContactsBook
from .Records import Record


class PhoneBookService:
    def __init__(self, book):
        self.__book: ContactsBook = book

    @property
    def book(self):
        return self.__book

    @book.setter
    def book(self, book: ContactsBook):
        self.book = book

    @error_handler
    def add_contact(self, args: list[str]):
        name, phone = args
        record = self.book.find(name)
        if record is None:
            if self.book.is_phone_owned(phone):
                raise PhoneAlreadyOwned(
                    f"This number {Fore.YELLOW}{phone}{Fore.RESET} already owned."
                )

            new_record = Record(name)  # type: ignore
            new_record.add_phone(phone)
            self.book.add_record(new_record)
            output_info(
                f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} with phone number {Fore.GREEN}{phone}{Fore.RESET} has been added."
            )
            return

        existing_phone = record.find_phone(phone)
        if existing_phone is None:
            record.add_phone(phone)
            output_info(
                f"New phone number {Fore.GREEN}{phone}{Fore.RESET} was added to {Fore.GREEN}{name.capitalize()}{Fore.RESET}."
            )
            return

        output_warning(
            f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} already has this number {Fore.GREEN}{phone}{Fore.RESET}"
        )

    @error_handler
    def change_contacts_phone(self, args) -> None:
        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found for name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        phone = record.find_phone(old_phone)
        if phone is None:
            raise FieldNotFound(
                f"Phone number {Fore.GREEN}{new_phone}{Fore.RESET} not exist. "
                / f"U can add it by using [{Fore.CYAN}add{Fore.RESET}] command, type help for more info."  # type: ignore
            )

        if self.book.is_phone_owned(new_phone):
            raise PhoneAlreadyOwned(
                f"This number {Fore.YELLOW}{new_phone}{Fore.RESET} already owned."
            )

        phone.value = new_phone
        output_info(
            f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} has been updated with new phone number {Fore.GREEN}{phone}{Fore.RESET}."
        )

    @error_handler
    def show_contacts_phones(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        print(self.book())  # type: ignore

    @error_handler
    def set_birthday(self, args):
        name, date = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        record.add_birthday(date)
        output_info(
            f"Contact's {Fore.GREEN}{name.capitalize()}{Fore.RESET} birthday was updated: {Fore.GREEN}{date}{Fore.RESET}."
        )

    @error_handler
    def get_birthday(self, args):
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found with name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        if record.birthday is None:
            output_warning(
                f"{Fore.GREEN}{name.capitalize()}{Fore.RESET} has not birthday setted."
            )

        output_info(
            f"{Fore.GREEN}{name.capitalize()}{Fore.RESET} has a birthday at: {Fore.GREEN}{str(record.birthday)}{Fore.RESET}"
        )

    @error_handler
    def show_next_week_birthdays(self):
        print(self.book.find_next_week_bithdays())

    @error_handler
    def show_all_contacts(self):
        print(self.book)

    # ====================================MAIL=====================================
    @error_handler
    def add_email(self, args: list[str]):
        name, email = args
        record = self.book.find(name)
        if record is None:
            new_record = Record(name)  # type: ignore
            new_record.add_email(email)
            self.book.add_record(new_record)
            output_info(
                f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} with email {Fore.GREEN}{email}{Fore.RESET} has been added."
            )
        else:
            if record.find_email(email) is None:
                record.add_email(email)
                output_info(
                    f"New email {Fore.GREEN}{email}{Fore.RESET} was added to {Fore.GREEN}{name.capitalize()}{Fore.RESET}."
                )
            else:
                output_warning(
                    f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} already has this email {Fore.GREEN}{email}{Fore.RESET}."
                )

    @error_handler
    def edit_email(self, args: list[str]):
        name, old_email, new_email = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found for name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        email_obj = record.find_email(old_email)
        if email_obj is None:
            raise FieldNotFound(
                f"Email {Fore.GREEN}{old_email}{Fore.RESET} not found. "
                f"Use add_email command to add it."
            )

        email_obj.value = new_email
        output_info(
            f"Contact {Fore.GREEN}{name.capitalize()}{Fore.RESET} has been updated with new email {Fore.GREEN}{new_email}{Fore.RESET}."
        )

    @error_handler
    def remove_email(self, args: list[str]):
        name, email = args
        record = self.book.find(name)
        if record is None:
            raise RecordNotFound(
                f"Record not found for name: {Fore.GREEN}{name}{Fore.RESET}"
            )

        email_obj = record.find_email(email)
        if email_obj is None:
            raise FieldNotFound(f"Email {Fore.GREEN}{email}{Fore.RESET} not found.")

        record.remove_email(email)
        output_info(
            f"Email {Fore.GREEN}{email}{Fore.RESET} removed from contact {Fore.GREEN}{name.capitalize()}{Fore.RESET}."
        )
